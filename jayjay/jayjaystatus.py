"""A simple script to change the status of the bot"""

import discord
import os

script_dir = os.path.dirname(__file__)

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

MESSAGE = os.getenv('MESSAGE')


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.change_presence(
        activity=discord.Activity(name=MESSAGE, type=discord.ActivityType.playing)
    )


def main():
    print(TOKEN)
    client.run(TOKEN)

if __name__ == '__main__':
    main()
