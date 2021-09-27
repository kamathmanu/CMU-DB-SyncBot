# Internal modules

import asyncio, os
from datetime import datetime
from dotenv import load_dotenv

# Third party modules

import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json

#Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
BOT_PREFIX = ("?", "!")
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Constants

SECONDS_IN_A_MIN = 60

# Configure discord bot

intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = Bot(command_prefix=BOT_PREFIX)

###########################################
### Event Handlers for Discord Bot
###########################################

def create_announcement(title, link, playAt):
    # countdownInMin = (playAt - datetime.now()).total_seconds() // SECONDS_IN_A_MIN
    announcement = "Today we continue with {}. Lecture will be in {} in 15 minutes!".format(title, link)
    return announcement

def create_date_from(timeStr : str):
    tokens = [int(timeField.strip()) for timeField in timeStr.split(',')] # yr, mth, date, hr, min
    return datetime(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])

@client.event
async def send_announcement(title, link, playAt):
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(create_announcement(title, link, playAt))

@client.event
async def on_ready():
    """
    Sets up scheduler, database for lecture playlist and annoucement schedule
    """
    announcementScheduler = AsyncIOScheduler()
    # lecturesInfo is a list which has extracted the relevant fields of each 
    lecturesInfo = [
        {"title": "Concurrency Control II", "url": "http://youtube.com/...1", "announceAt": "2021,9, 23, 21, 29", "playAt": "2021, 9, 25, 21, 15"},
        {"title": "Transactions", "url": "http://youtube.com/...transactions", "announceAt": "2021, 9, 23, 21, 33", "playAt": "2021, 9, 27, 21, 15"},
        {"title": "OLTP Indexes (Part I)", "url": "http://youtube.com/...oltp", "announceAt": "2021, 9, 23, 21, 39", "playAt": "2021, 9, 28, 21, 15"},
        {"title": "Query Optimization", "url": "http://youtube.com/...qopt", "announceAt": "2021, 9, 23, 21, 41", "playAt": "2021, 9, 30, 21, 15"},
    ]

    for jsonElement in lecturesInfo:

        videoTitle = jsonElement["title"]
        synctubeUrl = jsonElement["url"]
        announceAt = create_date_from(jsonElement["announceAt"])
        playAt = create_date_from(jsonElement["playAt"])

        announcementScheduler.add_job(send_announcement, trigger='date', run_date=announceAt, \
                                      args=[videoTitle, synctubeUrl, playAt])
    announcementScheduler.start()

if __name__ == '__main__':
    client.run(DISCORD_TOKEN)