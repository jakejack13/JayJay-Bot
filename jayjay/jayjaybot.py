"""The original script of JayJay. Can do simple commands like changing its status or nickname on a server"""

import discord
import random
import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()
sorry_num = 0  # used for !sorry


@client.event
async def on_message(message):  # bulk of command handling

    global sorry_num  # persistance bwteen command calls

    if message.author == client.user:  # prevents bot from replying to itself
        return

    if message.content.startswith("!hello"):  # hello (used to test bot)
        msg = f"Hello {message.author.mention}"
        await message.channel.send(msg)

    if message.content.startswith("!random"):  # random number 1-10
        randMsg = str(random.randint(1, 10))
        msg = f"Your random number from 1-10 is {randMsg}"
        await message.channel.send(msg)

    if message.content.startswith("!creator"):  # personal tag command
        msg = "I was created by JakeJack#3335. Say hi to him if you see him around!"
        await message.channel.send(msg)

    if message.content.startswith("!game"):  # change game presence of bot
        split = message.content.split(" ")
        msg = " ".join(split[1:])
        await client.change_presence(activity=discord.Game(name=msg))
        await message.add_reaction("\U0001F44D")

    if message.content.startswith("!name"):  # change nickname of bot on server
        split = message.content.split(" ")
        name = " ".join(split[1:])
        await message.guild.get_member(client.user.id).edit(nick=name)
        await message.add_reaction("\U0001F44D")

    if message.content.startswith("!sorry"):  # sorry counter command
        sorry_num += 1
        msg = f"Sorry, everyone. Sorry counter: {sorry_num}"
        await message.channel.send(msg)

    if message.content.startswith("!help"):  # list of commands
        msg = """CURRENT COMMANDS:
!hello
!random
!creator
!game
!name
!sorry
"""
        await message.channel.send(msg)

    if "as above, so below" in message.content.lower():  # as above, so below
        msg = "he shall return".format(message)
        await message.channel.send(msg)

        # DISCONTINUED COMMANDS

        # if message.content.startswith('!punish'): #spam ping command, discontinued
        #    split = message.content.split(' ')
        #    user = split[1]
        #    msg = 'Punishment time'.format(message)
        #    if user == "this" :
        #        while True :
        #            await message.channel.send(msg)
        #    else :
        #        while True :
        #            await message.guild.get_member(user).send(msg)

        # password: hewhoawaitshisname

        # if message.content.startswith('!nerd') : #comparing nerds, discontinued
        #    split = message.content.split(' ')
        #    other_user = split[1]
        #    first_user = message.author.mention
        #    rint = random.randint(0,1)
        #    if rint == 0 :
        #        msg = "" + first_user + " is nerdier than " + other_user
        #    else :
        #        msg = "" + other_user + " is nerdier than " + first_user
        #    await message.channel.send(msg)

        # if message.content.startswith("!kill"):  # shut down client
    #     msg = "\U0001F44D".format(message)
    #     await message.channel.send(msg)
    #     await client.logout()
    #     await client.close()


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