import discord
import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

HELP_STR = "Commands: help, message, dm, quit"


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
        print(HELP_STR)
        selection = input("> ")
        if selection == "help":
            print(HELP_STR)
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


def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
