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

    seconds = 1
    while seconds > 0:
        now = datetime.now()
        deadline = datetime(2021, 2, 20)
        seconds = floor((deadline - now).total_seconds())
        msg = str(seconds)
        await client.change_presence(activity=discord.Game(name=msg))
        print(msg)
        time.sleep(30)

    msg = "He returns"
    await client.change_presence(activity=discord.Game(name=msg))

client.run(TOKEN)
