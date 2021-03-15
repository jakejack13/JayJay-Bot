import discord
from datetime import datetime
from math import floor
import os

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir, token_path), "r")
TOKEN = f.read()
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


client.run(TOKEN)
