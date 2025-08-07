import asyncio
import feedparser
import sqlite3
import html
import hashlib
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

def hash_entry(entry):
    base = entry.get("id") or entry.get("link") or entry.get("title")
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def get_latest_news():
    random_sources = random.sample(RSS_SOURCES, len(RSS_SOURCES))

    for source in random_sources:
        feed = feedparser.parse(source)
        if not feed.entries:
            continue

        entry = sorted(feed.entries, key=lambda e: e.get("published_parsed", None), reverse=True)[0]
        news_id = hash_entry(entry)

        print(f"Checking hashed ID: {news_id}")

        cursor.execute("SELECT id FROM posted_news WHERE id = ?", (news_id,))
        if cursor.fetchone() is None:
            print("New news. Inserting...")

            try:
                cursor.execute("INSERT INTO posted_news (id) VALUES (?)", (news_id,))
                conn.commit()
            except sqlite3.IntegrityError as e:
                print(f"DB error: {e}")
                continue  # Skip on error

            title = entry.title
            link = entry.link
            description = clean_html(entry.get("summary", "")).replace("[…]", "").strip()

            news_item = f"<b>{title}</b>\n\n{description}\n\n{link}"
            return news_item
        else:
            print("Already posted.")

    return None

async def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")

if __name__ == "__main__":
    news = get_latest_news()
    if news:
        asyncio.run(send_to_telegram(news))
    conn.close()
