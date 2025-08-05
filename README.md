# TechDigestBotR 🤖

A Telegram bot that automatically collects and publishes the latest technology news to the [TechDigestBotR](https://t.me/TechDigestBotR) channel.

## Features

- Aggregates news from selected technology sources:
  - TechCrunch
  - The Verge
  - Ars Technica
- Uses a local SQLite database to prevent posting duplicate news
- Processes RSS feeds and selects only the most recent unpublished articles
- Publishes clean article titles and descriptions without promotional inserts
- Runs automatically on a defined schedule via **GitHub Actions**:
  - Weekdays — morning and evening
  - Weekends — midday

## How It Works

1. **News Parsing** — The bot fetches the latest articles from predefined RSS feeds.
2. **Duplicate Check** — Each article is compared with stored entries in the SQLite database to ensure it is not reposted.
3. **Publishing** — If the article is new, it is posted to the Telegram channel.

## Running the Bot

### Local Execution
1. Clone the repository:
   ```bash
   git clone https://github.com/yuladp1/telegram_bot.git
   cd telegram_bot
2. Create and configure config.py:

TOKEN = "your_bot_token"
CHANNEL_ID = "@your_channel_username"
3. Install dependencies:

pip install -r requirements.txt
4. Run:
python project.py

## Automated Deployment via GitHub Actions
Go to your repository settings on GitHub:
Settings → Secrets and variables → Actions

Add the following secrets:

TELEGRAM_TOKEN — Bot token obtained from BotFather

CHANNEL_ID — Channel ID or @username

The bot will be executed automatically according to the schedule defined in .github/workflows/news_bot.yml.

## Manual Run with GitHub Actions
To test the bot without waiting for the scheduled time:

Go to your repository on GitHub.

Navigate to Actions.

Select the workflow testdeploy.yml and click Run workflow.

Links
Telegram channel: TechDigestBotR