import discord
import time
from datetime import datetime, timedelta
from math import floor

f = open("token.txt", "r")
TOKEN = f.read()
client = discord.Client()


@client.event
async def on_ready():
    # message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = "the sunset"
    await client.change_presence(activity=discord.Activity(name=msg,type=discord.ActivityType.watching))

client.run(TOKEN)
