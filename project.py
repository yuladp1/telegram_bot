import asyncio
import feedparser
import sqlite3
import html
from telegram import Bot
#from config import TOKEN, CHANNEL_ID
import os
import random
# Define the RSS sources
RSS_SOURCES = [
    'https://techcrunch.com/feed/',
    'https://www.theverge.com/rss/index.xml',
    'https://feeds.arstechnica.com/arstechnica/index/'
]

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
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
    random_sources = random.sample(RSS_SOURCES, len(RSS_SOURCES))

    for source in random_sources:
        feed = feedparser.parse(source)
        if not feed.entries:
            continue

        entry = sorted(feed.entries, key=lambda e: e.get("published_parsed", None), reverse=True)[0]
        news_id = entry.link

        print(f"Checking news id: {news_id} from source: {source}")

        cursor.execute("SELECT id FROM posted_news WHERE id = ?", (news_id,))
        if cursor.fetchone() is None:
            print("New news found, inserting into DB.")
            cursor.execute("INSERT INTO posted_news (id) VALUES (?)", (news_id,))
            conn.commit()

            title = entry.title
            link = entry.link
            description = clean_html(entry.get("summary", ""))

            description = description.replace("[…]", "").strip()

            news_item = f"<b>{title}</b>\n\n{description}\n\n{link}"
            return news_item
        else:
            print("News already posted, skipping.")

    return None

async def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")

if __name__ == "__main__":
    news = get_latest_news()
    if news:
        asyncio.run(send_to_telegram(news))
    conn.close()
