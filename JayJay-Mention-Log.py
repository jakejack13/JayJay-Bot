import discord
f = open("token.txt","r")
TOKEN = f.read()
client = discord.Client()

log = open("log.txt","a")

@client.event
async def on_message(message):
    global log
    if message.guild.me in message.mentions:
        print(message.content + '\n')
        log.write(message.content + '\n')

    #if message.content.startswith('!kill') :
    #    msg = '\U0001F44D'.format(message)
    #    await message.channel.send(msg)
    #    log.close()
    #    await client.logout()ws
    #    await client.close()

@client.event
async def on_ready():
    #message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = "Ping me to send a message to JakeJack"
    await client.change_presence(activity=discord.Game(name=msg))

#client.loop.create_task(my_background_task())
client.run(TOKEN)
