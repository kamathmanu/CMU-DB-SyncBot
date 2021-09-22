# Design Doc for Bot

## Overview

The bot will need to:

- Mark availability via calendar to set periods/frequency
- Send out announcement every given period which link to SyncTube
- Pick correct YouTube video from the PlayList and host on SyncTube
- Send out reminder announcement(s) prior to the lecture vid
- Disable chat
- Assign moderator users (??)

## Discord API:

- Creating a bot for a guild
- Posting announcements periodically to guild

Get started with [Bot basics](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python).

Bot Scopes:

- Manage webhooks, View channels ??
- Text permissions: Send messages, Mention everyone
- 

## Scheduling posts for each lecture day

Use the APScheduler API for this. [API Guide](https://apscheduler.readthedocs.io/en/3.x/userguide.html)

What is a job in this case?

1. Submitting a specific lecture video link to synctube.
2. Simply posting the announcement with the synctube link based on the schedule ()

- `AsyncIOScheduler`
- Which job store?
- `ThreadPoolExecutor`
- Trigger: `date` makes the most sense, should we combine triggers? date and cron maybe?




