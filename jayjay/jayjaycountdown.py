"""Counts down to a specified time in its status"""

import discord
from datetime import datetime
from math import floor
import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()


@client.event
async def on_message(message):
    now = datetime.now()
    deadline = datetime(2021, 2, 20)
    seconds = floor((deadline - now).total_seconds())
    msg = str(seconds)
    await client.change_presence(activity=discord.Game(name=msg))
    print(msg)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()