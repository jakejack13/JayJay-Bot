import discord

f = open("token.txt", "r")
TOKEN = f.read()
client = discord.Client()
m = open("message.txt","r")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = m.read()
    await client.change_presence(activity=discord.Activity(name=msg,type=discord.ActivityType.playing))
    corner = client.get_channel(756953581671940147)
    await corner.connect()

client.run(TOKEN)
