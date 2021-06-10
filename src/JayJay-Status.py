import asyncio
import discord
import os

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir, token_path), "r")
TOKEN = f.read()
client = discord.Client()
message_path = "../lib/message.txt"
m = open(os.path.join(script_dir, message_path), "r")
msg = m.read()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.change_presence(
        activity=discord.Activity(name=msg, type=discord.ActivityType.playing)
    )


client.run(TOKEN)
