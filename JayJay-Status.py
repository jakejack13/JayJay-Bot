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

    while True :
        msg = input('> ')
        #msg = "Time"
        await client.change_presence(activity=discord.Game(name=msg))

client.run(TOKEN)
