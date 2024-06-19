# CherzyCoinBot

## Project Overview

This project involves creating a powerful bot using Python, which fetches real-time cryptocurrency prices and delivers them through Telegram. The bot is deployed on an AWS EC2 instance to ensure continuous operation, leveraging PuTTY and Ubuntu for setup and management.

## 1. Setting Up the Telegram Bot

### 1.1. Creating the Telegram Bot

1. **Create a Telegram Bot**:
   - Open Telegram and search for "BotFather".
   - Start a chat with BotFather and use the command `/newbot` to create a new bot.
   - Follow the prompts to give your bot a name and username.
   - BotFather will provide you with a token. Save this token; you will need it later.

2. **Get Your Chat ID**:
   - Start a chat with your bot and send a message.
   - Visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates` in a web browser, replacing `<YourBOTToken>` with your actual bot token.
   - Look for `"chat": {"id": <YourChatID>}` in the JSON response to find your chat ID.

### 1.2. Coding the Telegram Bot

1. **Install Required Libraries**:
   ```sh
   pip install python-telegram-bot aiohttp
