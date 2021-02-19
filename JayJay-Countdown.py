import discord
import time
from datetime import datetime, timedelta
from math import floor

f = open("token.txt", "r")
TOKEN = f.read()
client = discord.Client()

@client.event
async def on_message(message) :
    now = datetime.now()
    deadline = datetime(2021, 2, 20)
    seconds = floor((deadline - now).total_seconds())
    msg = str(seconds)
    await client.change_presence(activity=discord.Game(name=msg))
    print(msg)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
