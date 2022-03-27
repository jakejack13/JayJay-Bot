import discord
import os
from discord.ext import commands
import asyncio

from typing import List

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix="!")


def flatten(lst: List[str]) -> str:
    result = ""
    for s in lst:
        result += s + " "
    return result


class StringIter:
    def __init__(self, string: str):
        spl = string.split(" ")
        self.lst = [flatten(spl[: i + 1]) for i in range(len(spl))]

    def __iter__(self):
        return self.lst.__iter__()


async def iter_status(msg: str):
    for s in StringIter(msg):
        print(s)
        await client.change_presence(
            activity=discord.Activity(name=s, type=discord.ActivityType.playing)
        )
        await asyncio.sleep(2.5)


async def main_loop():
    while True:
        msg = input("> ")
        await iter_status(msg)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await main_loop()


client.run(TOKEN)
