# Internal modules

import asyncio, os
from datetime import datetime
from dotenv import load_dotenv

# Third party modules

import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

#Load environment variables

send_time='20:15' #time is in 24hr format

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
BOT_PREFIX = ("?", "!")
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Constants

SECONDS_IN_A_MIN = 60
N = 2 * SECONDS_IN_A_MIN

# Configure discord bot

intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = Bot(command_prefix=BOT_PREFIX)

###########################################
### Lecture Annoucement
###########################################

def create_announcement(link, time):
    return ""

async def send_announcement(link, time):
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(create_announcement(link, time))

###########################################
### Event Handlers for Discord Bot
###########################################

@client.event
async def on_ready():

    announcement_scheduler = AsyncIOScheduler()
    # announcement_scheduler.add_jobstore()
    # announcement_scheduler.add_executor()
    # announcement_scheduler.add_listener()
    # scheduler.add_job(func, CronTrigger(hour="24", minute="0", second="0")) 
    # announcement_scheduler.start()

@tasks.loop(seconds=N)
async def called_every_n_min():
    message = "Testing!"
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)

@called_every_n_min.before_loop
async def before():
    await client.wait_until_ready()
    print("Sending announcement")

if __name__ == '__main__':
    called_every_n_min.start()
    client.run(DISCORD_TOKEN)