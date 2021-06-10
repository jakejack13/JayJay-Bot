from time import sleep
import discord
import os
from discord.ext import commands
import asyncio

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir, token_path), "r")
TOKEN = f.read()
client = commands.Bot(command_prefix="!")


async def color_change():
    await client.wait_until_ready()
    pisscord = await client.fetch_guild(813866062495481872)
    role: discord.Role = pisscord.get_role(844706451905708083)
    while True:
        await role.edit(colour=discord.Colour.random())
        await asyncio.sleep(1.5)


@client.event
async def on_ready():
    channel = await client.fetch_channel(840737842871271464)
    while True:
        await channel.send("<@547910268081143830>")
        await asyncio.sleep(0.6)


client.run(TOKEN)
