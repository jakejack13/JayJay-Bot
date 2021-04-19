import discord
import os
import asyncio
import random
import time

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir, token_path), "r")
TOKEN = f.read()
client = discord.Client()


async def change_nickname():
    """Changes the nicknames of members of the selected role"""
    await client.wait_until_ready()
    list_of_nicknames = [
        "test1",
        "test2",
        "test3",
        "test4",
        "test5",
        "test6",
        "test7",
    ]
    while True:
        for nickname in list_of_nicknames:
            server = await client.fetch_guild(813866062495481872)
            role: discord.Role = server.get_role(828403520402358283)
            member: discord.Member
            for member in role.members:
                print(member)
                member.edit(nick=nickname)


async def ping_loop():
    """Repeatedly pings the members of the selected roles"""
    await client.wait_until_ready()
    server = await client.fetch_guild(813866062495481872)
    role: discord.Role = server.get_role(828403520402358283)
    role_mention = role.mention
    channel = await client.fetch_channel(813866062495481875)
    while True:
        await asyncio.sleep(0.8)
        await channel.send(role_mention)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    msg = "Hmmm"
    await client.change_presence(
        activity=discord.Activity(name=msg, type=discord.ActivityType.playing)
    )
    # await ping_loop()
    # await change_nickname()


client.loop.create_task(ping_loop())
client.loop.create_task(change_nickname())
client.run(TOKEN)
