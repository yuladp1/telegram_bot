import asyncio
import feedparser
import sqlite3
import html
from telegram import Bot
#from config import TOKEN, CHANNEL_ID
import os
# Define the RSS sources
RSS_SOURCES = [
    'https://techcrunch.com/feed/',
    'https://www.theverge.com/rss/index.xml',
    'https://feeds.arstechnica.com/arstechnica/index/'
]

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
# Initialize the database connection
conn = sqlite3.connect('news.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS posted_news (
    id TEXT PRIMARY KEY
)
''')
conn.commit()

def clean_html(raw_html):
    import re
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext).strip()

def get_latest_news():
    for source in RSS_SOURCES:
        feed = feedparser.parse(source)
        for entry in feed.entries:
            news_id = entry.link
            cursor.execute("SELECT id FROM posted_news WHERE id = ?", (news_id,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO posted_news (id) VALUES (?)", (news_id,))
                conn.commit()

                title = entry.title
                link = entry.link
                description = clean_html(entry.get("summary", ""))

                if "TechCrunch" in source and description.startswith("Welcome back to TechCrunch"):
                    description = ". ".join(description.split(".")[1:]).strip()

                description = description.replace("[…]", "").strip()

                return f"{title}\n\n{description}\n\n{link}"
    return None

async def send_to_telegram(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=message)

if __name__ == "__main__":
    news = get_latest_news()
    if news:
        asyncio.run(send_to_telegram(news))
    else:
        print("No new news to post.")
    conn.close()
