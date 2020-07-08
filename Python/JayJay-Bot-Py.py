import discord
import random
TOKEN = "NDAwMTE5NTUzMTM4NjIyNDg0.DTXBAQ.XZ_UFCOySPa7MwVT37krX3gis-E"
client = discord.Client()

@client.event
async def on_message(message):
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
        msg = split[1]
        await client.change_presence(activity=discord.Game(name=msg))
        await message.add_reaction(discord.Reaction.emoji('\U0001F44D'))
    if message.content.startswith('!punish'):
        split = message.content.split(' ')
        user = split[1]
        msg = 'Punishment time'.format(message)
        if user == "this" :
            while True :
                await message.channel.send(msg)
        else :
            while True :
                await message.guild.get_member(user).send(msg)
    if message.content.startswith('!kill') :
        msg = '\U0001F44D'.format(message)
        await message.channel.send(msg)
        await client.logout()
        await client.close()

@client.event
async def on_ready():
    #message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#client.loop.create_task(my_background_task())
client.run(TOKEN)
