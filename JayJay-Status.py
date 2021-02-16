import discord
import time
from datetime import datetime, timedelta
from math import floor

f = open("token.txt", "r")
TOKEN = f.read()
client = discord.Client()
m = open("message.txt","r")

@client.event
async def on_ready():
    # message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = m.read()
    await client.change_presence(activity=discord.Activity(name=msg,type=discord.ActivityType.playing))
    corner = client.get_channel(756953581671940147)
    await corner.connect()

client.run(TOKEN)
