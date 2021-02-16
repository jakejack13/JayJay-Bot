import discord
import random

import sys
import io
import os

f = open("token.txt", "r")
TOKEN = f.read()
client = discord.Client()
sorry_num = 0  # used for !sorry

def search(list, elem):
    for i in range (len(list)):
        if list[i] == elem:
            return i
    return -1

@client.event
async def on_message(message):  # bulk of command handling

    global sorry_num  # persistance bwteen command calls

    if message.author == client.user:  # prevents bot from replying to itself
        return

    if message.content.startswith('!hello'):  # hello (used to test bot)
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!random'):  # random number 1-10
        randMsg = str(random.randint(1, 10))
        msg = ('Your random number from 1-10 is ' + randMsg).format(message)
        await message.channel.send(msg)

    if message.content.startswith('!creator'):  # personal tag command
        msg = 'I was created by JakeJack#3335. Say hi to him if you see him around!'.format(
            message)
        await message.channel.send(msg)

    if message.content.startswith('!game'):  # change game presence of bot
        split = message.content.split(' ')
        msg = " ".join(split[1:])
        await client.change_presence(activity=discord.Game(name=msg))
        await message.add_reaction('\U0001F44D')

    if message.content.startswith('!name'):  # change nickname of bot on server
        split = message.content.split(' ')
        name = " ".join(split[1:])
        await message.guild.get_member(client.user.id).edit(nick=name)
        await message.add_reaction('\U0001F44D')

    if message.content.startswith('!kill'):  # shut down client
        msg = '\U0001F44D'.format(message)
        await message.channel.send(msg)
        await client.logout()
        await client.close()

    if message.content.startswith('!sorry'):  # sorry counter command
        sorry_num += 1
        msg = ("Sorry, everyone. Sorry counter: " +
               str(sorry_num)).format(message)
        await message.channel.send(msg)
    
    if message.content.startswith('!python'):
        old_stdout = sys.stdout # Memorize the default stdout stream
        sys.stdout = buffer = io.StringIO()

        split = message.content.split(' ')
        msg = " ".join(split[1:])
        clean_msg = msg.replace('`','')
        exec(compile(clean_msg,"text.txt","exec"))

        whatWasPrinted = buffer.getvalue()
        sys.stdout = old_stdout
        await message.channel.send(whatWasPrinted)

    if message.content.startswith('!java'):
        split = message.content.split(' ')
        msg = " ".join(split[1:])
        class_name = split[search(split,"class") + 1]
        clean_msg = msg.replace('`','')
        
        os.system("rm -f *.java *.class")
        os.system("echo \"" + msg + "\" > " + class_name + ".java")
        os.system("javac " + class_name + ".java")
        stream = os.popen("java " + class_name)
        output = stream.read()

        await message.channel.send(output)

    if message.content.startswith('!c'):
        split = message.content.split(' ')
        msg = " ".join(split[1:])
        clean_msg = msg.replace('`','')

        os.system("rm -f *.c *.out")
        os.system("echo \"" + msg + "\" > main.c")
        os.system("gcc main.c")
        stream = os.popen("./a.out")
        output = stream.read()

        await message.channel.send(output)

    if message.content.startswith('!brainfuck'):
        split = message.content.split(' ')
        msg = " ".join(split[1:])
        clean_msg = msg.replace('`','')

        os.system("rm -f *.bf")
        os.system("echo \"" + msg + "\" > main.bf")
        stream = os.popen("brainfuck main.bf")
        output = stream.read()

        await message.channel.send(output)

    
    if message.content.startswith('!help'):  # list of commands
        msg = """CURRENT COMMANDS:
!hello
!random
!creator
!game
!name
!sorry
!python
!java
!c
!brainfuck
Secret command to break the bot""".format(message)
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


@client.event
async def on_ready():
    # message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = "Status: Online"
    await client.change_presence(activity=discord.Game(name=msg))
    corner = client.get_channel(756953581671940147)
    await corner.connect()

client.run(TOKEN)

