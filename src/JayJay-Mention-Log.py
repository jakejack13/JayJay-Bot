import discord
import os

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir,token_path), "r")
TOKEN = f.read()
client = discord.Client()
log_path = "../lib/log.txt"
f = open(os.path.join(script_dir,log_path), "r")


@client.event
async def on_message(message):

    global log  # file state persistance

    if message.guild.me in message.mentions:  # log message
        print(message.content + '\n')
        log.write(message.content + '\n')

    # if message.content.startswith('!kill') : # stop bot and save log (not necessary on CLI)
    #    msg = '\U0001F44D'.format(message)
    #    await message.channel.send(msg)
    #    log.close()
    #    await client.logout()
    #    await client.close()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = "Jake can't come to the phone right now. Ping JayJay to leave a message"
    await client.change_presence(activity=discord.Game(name=msg))

client.run(TOKEN)
