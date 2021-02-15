import discord
import time
from datetime import datetime, timedelta
from math import floor

f = open("token.txt", "r")
TOKEN = f.read()
client = discord.Client()


@client.event
async def on_message(message) :
    msg = input('> ')
    await client.change_presence(activity=discord.Game(name=msg))
    print(msg)



@client.event
async def on_ready():
    # message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
