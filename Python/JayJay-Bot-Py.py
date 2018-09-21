import discord
import asyncio
import random
TOKEN = "NDAwMTE5NTUzMTM4NjIyNDg0.DTXBAQ.XZ_UFCOySPa7MwVT37krX3gis-E"
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_message(message):
    if message.content.startswith('!private'):
        msg = "Hello {0.author.mention}".format(message)
        await client.send_message(message.author,msg)

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id='363801910970548266')
    while not client.is_closed:
        counter += 1
        songs = open("songs.txt", "r")
        song_num = random.randint(0,20)
        song = songs.readlines()
        msg = song[song_num]
        await client.send_message(channel, msg)
        await asyncio.sleep(60) # task runs every 60 seconds

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run(TOKEN)
