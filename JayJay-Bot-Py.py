import discord
import random
f = open("token.txt","r")
TOKEN = f.read()
client = discord.Client()


sorry_num = 0
send = 0

@client.event
async def on_message(message):
    global send
    global sorry_num
    #prevents bot from replying to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!random'):
        randMsg = str(random.randint(1,10))
        msg = ('Your random number from 1-10 is ' + randMsg).format(message)
        await message.channel.send(msg)
    if message.content.startswith('!creator'):
        msg = 'I was created by JakeJack#3335. Say hi to him if you see him around!'.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!game'):
        split = message.content.split(' ')
        msg = " ".join(split[1:])
        await client.change_presence(activity=discord.Game(name=msg))
        await message.add_reaction('\U0001F44D')
    if message.content.startswith('!name') :
        split = message.content.split(' ')
        name = " ".join(split[1:])
        await message.guild.get_member(client.user.id).edit(nick=name)
        await message.add_reaction('\U0001F44D')
    #if message.content.startswith('!punish'):
    #    split = message.content.split(' ')
    #    user = split[1]
    #    msg = 'Punishment time'.format(message)
    #    if user == "this" :
    #        while True :
    #            await message.channel.send(msg)
    #    else :
    #        while True :
    #            await message.guild.get_member(user).send(msg)
    if message.content.startswith('!kill') :
        msg = '\U0001F44D'.format(message)
        await message.channel.send(msg)
        await client.logout()
        await client.close()
    #if message.content.startswith('!nerd') :
    #    split = message.content.split(' ')
    #    other_user = split[1]
    #    first_user = message.author.mention
    #    rint = random.randint(0,1)
    #    if rint == 0 :
    #        msg = "" + first_user + " is nerdier than " + other_user
    #    else :
    #        msg = "" + other_user + " is nerdier than " + first_user
    #    await message.channel.send(msg)
    if message.content.startswith('!sorry') :
        sorry_num+=1
        msg = ("Sorry, everyone. Sorry counter: " + str(sorry_num)).format(message)
        await message.channel.send(msg)
    #if message.content.startswith('!help') :
        #msg = """CURRENT COMMANDS:
#!hello
#!random
#!creator
#!game
#!name
#!sorry
#Secret command to break the bot""".format(message)
        #await message.channel.send(msg)

    if "as above, so below" in message.content.lower() :
        msg = "he shall return".format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    #message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = "as above, so below"
    await client.change_presence(activity=discord.Game(name=msg))

#client.loop.create_task(my_background_task())
client.run(TOKEN)
