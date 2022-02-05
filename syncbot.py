# Internal modules

import asyncio, os
from datetime import datetime
from dotenv import load_dotenv

# Third party modules

import json
import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
BOT_PREFIX = ("?", "!")
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')
BROWSER_BINARY_PATH = os.getenv('BROWSER_BINARY_PATH')

# Constants

SECONDS_IN_A_MIN = 60
SYNCTUBE_NEWROOM_URL = "https://sync-tube.de/create"

# Selenium API - Chromium assumed but can easily modify to browser of choice

chromiumOptions = webdriver.ChromeOptions()
chromiumOptions.binary_location = BROWSER_BINARY_PATH
# chromiumOptions.add_argument("--headless")

# Configure discord bot

intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = Bot(command_prefix=BOT_PREFIX)

###########################################
### Handlers for Selenium Video Syncing
###########################################

async def prepare_synctube_room(chromeDriver, room, youtubeUrl):
    
    # get the searchbar, and simulate a click followed by the entering of the youtubeUrl
    WebDriverWait(chromeDriver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input.searchInput')))
    searchBarElement = chromeDriver.find_element_by_css_selector('input.searchInput')
    searchBarElement.click()
    searchBarElement.send_keys(youtubeUrl)
    searchBarElement.send_keys(Keys.ENTER)
    
    # restrict guests from adding members or commenting
    chromeDriver.find_element_by_id('btnSettings').click()
    
    chromeDriver.find_element_by_css_selector(\
        '#table_permissions > tbody > tr:nth-child(2) > td:nth-child(2) > #\\30').click() # Add => Guest turned off

    chromeDriver.find_element_by_css_selector(\
        '#table_permissions > tbody > tr:nth-child(8) > td:nth-child(2) > #\\30').click() # Use Chat => Guest turned off
    
    # close the settings page
    closeSettings = chromeDriver.find_element_by_css_selector('body > div > div.settings.settings_visible > div.btnClose > img')
    closeSettings.click()

    player_status = chromeDriver.execute_script("return document.getElementsByClassName('html5-video-player')[0].getPlayerState()")
    await player_status == 0

async def sync_video(youtubeUrl):
    """
    Creates a room in sync-tube.de for a given youtubeUrl
    Returns the URL for the synctube room created
    """
    # reach the creation page for a new room
    chromeDriver = webdriver.Chrome(options=chromiumOptions, executable_path=WEBDRIVER_PATH)
    chromeDriver.get(SYNCTUBE_NEWROOM_URL)
    """asyncio.run("""
    await prepare_synctube_room(chromeDriver, chromeDriver.current_url, youtubeUrl)

    chromeDriver.ex
    # chromeDriver.quit()

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
    # client.run(DISCORD_TOKEN)
    asyncio.run(sync_video("https://www.youtube.com/watch?v=oeYBdghaIjc&list=PLSE8ODhjZXjbohkNBWQs_otTrBTrjyohi"))


    