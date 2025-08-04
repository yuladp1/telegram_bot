# Tech News Telegram Bot

You can interact with the bot directly via Telegram: [TechDigestBotR](https://t.me/TechDigestBotR)

This Telegram bot automatically fetches technology news from multiple RSS feeds and posts them to a Telegram channel on a schedule. The goal is to provide concise, fresh tech news updates 1-2 times per day.

---

## Features

- Automatically fetches news from several tech RSS sources.
- Parses and shortens news content for Telegram-friendly posts.
- Avoids duplicate posts by storing published news in an SQLite database.
- Scheduled posting on weekdays and weekends at specific times.
- Simple setup with configuration separated into a `config.py` file.

---

## News Sources

- [TechCrunch](https://techcrunch.com/feed/)
- [The Verge](https://www.theverge.com/rss/index.xml)
- [ArsTechnica](http://feeds.arstechnica.com/arstechnica/index)

---

## Posting Schedule

- Weekdays (Monday to Friday): 9:00 AM and 7:00 PM
- Weekends (Saturday and Sunday): 12:00 PM

---

## How the bot selects news for posting

1. The bot fetches all fresh news from the configured RSS sources.

2. It filters out the news that have already been published (checking against the SQLite database).

3. It picks the first news item from the list (RSS feeds usually provide news in order from newest to oldest).

4. This way, the bot publishes the freshest news that has not been posted before.

---

## How to Run

1. Install required packages listed in `requirements.txt`.

2. Create and configure `config.py` with your Telegram bot token and channel ID.
```python
# config.py

# Telegram bot token from BotFather
TOKEN = "YOUR_BOT_TOKEN"

# Telegram channel ID (for public channels use @channelusername, 
# for private channels use numeric ID starting with -100)
CHANNEL_ID = -100XXXXXXXXXX

3. Run the main script to test posting manually or run it as a scheduled job.

---

## Project Structure

- `project.py` — main bot script
- `config.py` — configuration file with bot token and channel ID (excluded from Git)
- `requirements.txt` — list of Python dependencies
- `news.db` — SQLite database file created at runtime

---

## Notes

- The bot posts one news item per scheduled run.
- You can expand the sources or customize the post formatting.
- Use SQLite database for persistence of published news to avoid duplicates.

---