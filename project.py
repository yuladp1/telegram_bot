import asyncio
from telegram import Bot
import feedparser
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# Load configuration
import config  # TELEGRAM_TOKEN and CHANNEL_ID should be in config.py

bot = Bot(token=config.TOKEN)

# Connect to SQLite database
conn = sqlite3.connect('news.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS news (
    link TEXT PRIMARY KEY
)
''')
conn.commit()

# RSS sources
RSS_SOURCES = [
    'https://techcrunch.com/feed/',
    'https://www.theverge.com/rss/index.xml',
    'http://feeds.arstechnica.com/arstechnica/index'
]

async def fetch_and_post_news():
    print(f"[{datetime.now()}] Checking for news...")

    for url in RSS_SOURCES:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # take up to 5 latest news from each source
            link = entry.link
            cursor.execute('SELECT 1 FROM news WHERE link = ?', (link,))
            if cursor.fetchone():
                continue  # news already posted

            # Clean description from HTML and ads
            description = entry.get('summary', '') or entry.get('description', '')
            description = clean_description(description)

            # Prepare post text
            post_text = f"📰 *{entry.title}*\n\n{description}\n\n[Read more]({link})"

            try:
                await bot.send_message(chat_id=config.CHANNEL_ID, text=post_text, parse_mode='Markdown', disable_web_page_preview=True)
                print(f"Posted news: {entry.title}")
                cursor.execute('INSERT INTO news (link) VALUES (?)', (link,))
                conn.commit()
            except Exception as e:
                print(f"Error sending news: {e}")

def clean_description(text):
    import re
    # Remove HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)

    # Optionally remove unwanted phrases (ads, repeated intros, etc.)
    unwanted_phrases = [
        "Welcome back to TechCrunch Mobility",
        "You might find it kind of sad",
        "…",
        "Read more on the site",
        "Source:",
    ]
    for phrase in unwanted_phrases:
        cleantext = cleantext.replace(phrase, '')

    # Trim text to 300 characters without cutting words
    if len(cleantext) > 300:
        cleantext = cleantext[:300]
        if ' ' in cleantext:
            cleantext = cleantext.rsplit(' ', 1)[0]
        cleantext += '...'

    return cleantext.strip()

def schedule_jobs():
    scheduler = AsyncIOScheduler()

    # Schedule posts on weekdays at 9:00 and 19:00
    scheduler.add_job(fetch_and_post_news, 'cron', day_of_week='mon-fri', hour=9, minute=0)
    scheduler.add_job(fetch_and_post_news, 'cron', day_of_week='mon-fri', hour=19, minute=0)

    # Schedule posts on Saturday and Sunday at 12:00
    scheduler.add_job(fetch_and_post_news, 'cron', day_of_week='sat,sun', hour=12, minute=0)

    scheduler.start()

async def main():
    schedule_jobs()
    print("Bot started and waiting for scheduled posts...")
    while True:
        await asyncio.sleep(3600)  # keep the program running

if __name__ == '__main__':
    asyncio.run(main())
