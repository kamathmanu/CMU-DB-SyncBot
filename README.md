# CMU DB Lectures SyncBot

A bot that automates playing of lectures (or any playlist of videos) on SyncTube and notifies the automated schedule on Discord.

## Setup

`pip install -U python-dotenv`
`pip install -U discord`

Make sure your chromedriver is the same version as your browser (NOTE: if your browser updates versions, you need to update chrome WebDriver too)

Your .env file should consist of the following (simply add and `=<value>` to each field, no spaces)

- DISCORD_TOKEN : refer to Discord API for this
- DISCORD_GUILD : the Discord Server to add the bot to
- CLIENT_ID : refer to Discord API for this
- CHANNEL_ID : refer to Discord API for this
- CHANNEL_NAME : The channel in your server to add the bot to
- WEBDRIVER_PATH : Where your selenium webdriver is located
- BROWSER_BINARY_PATH : where the binary for your browser (Chromium assumed) is stored

[Discord Bot API Crash Course](https://realpython.com/how-to-make-a-discord-bot-python/)