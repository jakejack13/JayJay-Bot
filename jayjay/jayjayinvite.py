import discord
import os
from discord.channel import TextChannel, VoiceChannel
from discord.ext import commands

from typing import *

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()
client = commands.Bot(command_prefix="!")

SERVER_ID = 716231232635011074
VOICE_CHANNEL_ID = 869940658289410069
TEXT_CHANNEL_ID = 807085305739870249
JAKEJACK = 139126745159827457


async def add_member_perms(mem_id: int, server_id: int, voice_channel_id: int):
    server = await client.fetch_guild(server_id)
    member = await server.fetch_member(mem_id)
    channel: VoiceChannel = await client.fetch_channel(voice_channel_id)
    overwrite = discord.PermissionOverwrite()
    overwrite.connect = True
    await channel.set_permissions(member, overwrite=overwrite)


async def remove_member_perms(mem_id: int, server_id: int, voice_channel_id: int):
    server = await client.fetch_guild(server_id)
    member = await server.fetch_member(mem_id)
    channel: VoiceChannel = await client.fetch_channel(voice_channel_id)
    await channel.set_permissions(member, overwrite=None)


async def message_member(
    mem_id: int, server_id: int, text_channel_id: int, voice_channel_id: int
):
    server = await client.fetch_guild(server_id)
    member = await server.fetch_member(mem_id)
    text_channel: TextChannel = await client.fetch_channel(text_channel_id)
    voice_channel: VoiceChannel = await client.fetch_channel(voice_channel_id)
    msg = f"{member.mention}, you have been requested to join {voice_channel.mention}"
    await text_channel.send(msg)


@client.event
async def on_voice_state_update(member, before, after):
    if (
        before.channel
        and before.channel != after.channel
        and before.channel.id == VOICE_CHANNEL_ID
    ):
        await remove_member_perms(member.id, SERVER_ID, VOICE_CHANNEL_ID)


@client.event
async def on_message(message):
    if message.author.id == JAKEJACK and message.content.startswith("!invite"):
        mem_id = int(message.content.split(" ")[1])
        await message_member(mem_id, SERVER_ID, TEXT_CHANNEL_ID, VOICE_CHANNEL_ID)
        await add_member_perms(mem_id, SERVER_ID, VOICE_CHANNEL_ID)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
    