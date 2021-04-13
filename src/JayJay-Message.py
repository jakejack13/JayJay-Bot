import discord
import os

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir, token_path), "r")
TOKEN = f.read()
client = discord.Client()

help_str = "Commands: help, message, dm, quit"


async def dm_loop():
    print("Please input the user id")
    try:
        user_id = int(input("> "))
        user = await client.fetch_user(user_id)
        user_channel = await user.create_dm()
        print("Connected to user " + str(user_id))
        while True:
            message = input("> ")
            if message == "quit":
                break
            else:
                await user_channel.send(message)
    except:
        print("Incorrect user id, please try again")


async def message_loop():
    print("Please input the channel id")
    try:
        channel_id = int(input("> "))
        channel = await client.fetch_channel(channel_id)
        print("Connected to channel " + str(channel_id))
        while True:
            message = input("> ")
            if message == "quit":
                break
            else:
                await channel.send(message)
    except:
        print("Incorrect channel id, please try again")


async def main_loop():
    while True:
        print(help_str)
        selection = input("> ")
        if selection == "help":
            print(help_str)
        elif selection == "message":
            await message_loop()
        elif selection == "dm":
            await dm_loop()
        elif selection == "quit":
            break
        else:
            print("Incorrect command, please try again")
    await client.close()


@client.event
async def on_ready():
    print("Welcome, JayJay")
    await main_loop()


client.run(TOKEN)
