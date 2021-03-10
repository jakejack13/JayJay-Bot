import asyncio
import discord
import os
import gachapy.objects, gachapy.controller, gachapy.loader


script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir,token_path), "r")
TOKEN = f.read()
client = discord.Client()

item_file = "/mnt/c/Users/JCKB1/Documents/GitHub/JayJay-Bot/lib/items.json"
banner_file = "/mnt/c/Users/JCKB1/Documents/GitHub/JayJay-Bot/lib/banners.json"
player_file = "/mnt/c/Users/JCKB1/Documents/GitHub/JayJay-Bot/lib/players.json"
controller = gachapy.loader.load_controller(item_file,banner_file,player_file)

async def save() :
    while True :
        gachapy.loader.save_controller(controller,item_file,banner_file,player_file)
        await asyncio.sleep(60)

async def create_gachas() :
    while True :
        controller.remove_all_banners()
        controller.create_random_banner("A",5)
        controller.create_random_banner("B",5)
        counter = 10
        while counter > 0 :
            counter -= 1
            msg = str(counter) + " mins until next banner refresh"
            try :
                await client.change_presence(activity=discord.Game(name=msg))
            except :
                msg = ""
            await asyncio.sleep(60)

async def check_user(user) :
    name = user.name + "#" + user.discriminator
    user_item = controller.find_item(name)
    if user_item == None :
        controller.add_new_item(name,str(user.id),1)
    else :
        user_item.rarity += 1
    user_player = controller.find_player(name)
    if user_player == None :
        controller.add_new_player(name,100)
    else :
        top_player = controller.top_players(2)[0]
        top_item = controller.top_items(2)[0]
        controller.change_money_player(name,top_player.get_net_worth() / top_item.rarity)

@client.event
async def on_message(message): 
    if message.author == client.user:
        return

    if message.content.startswith("!help") :
        msg = """COMMANDS:
        !inventory
        !info
        !banners
        !top
        !pull
        """.format(message)
        await message.channel.send(msg)

    if message.content.startswith("!pull") :
        split = message.content.split(' ')
        if len(split) < 2 :
            msg = "Usage: !pull <name of banner>"
        else :
            try :
                item = controller.pull(message.author.name + "#" + message.author.discriminator,split[1])
                if item == None :
                    msg = "You do not have enough money to pull from this banner"
                else :
                    msg = "You pulled:\n" + str(item)
            except gachapy.controller.PullError as e:
                msg = str(e)
        
        await message.channel.send(msg)

    if message.content.startswith("!info") :
        split = message.content.split(' ')
        if len(split) < 3 :
            msg = "Usage: !info <item/banner/player> <name>"
        elif split[1] == "item" :
            item = controller.find_item(" ".join(split[2:]))
            if item == None :
                msg = "Item not found".format(message)
            else :
                msg = str(item).format(message)
        elif split[1] == "banner" :
            banner = controller.find_banner(" ".join(split[2:]))
            if banner == None :
                msg = "Banner not found".format(message)
            else :
                msg = str(banner).format(message)
        elif split[1] == "player" :
            player = controller.find_player(" ".join(split[2:]))
            if player == None :
                msg = "Item not found".format(message)
            else :
                msg = str(player).format(message)
        else :
            msg = "Usage: !info <item/banner/player> <name>"
        await message.channel.send(msg)
        
    if message.content.startswith("!banners") :
        msg = ""
        for banner in controller.banners :
            msg += str(banner) + "\n"
            msg += "\n"
        msg = msg.format(message)
        await message.channel.send(msg)
    
    if message.content.startswith("!top") :
        split = message.content.split(' ')
        if len(split) < 2 :
            msg = "Usage: !top <item/player>"
        elif split[1] == "item" :
            top_items = controller.top_items(10)
            msg = ""
            for item in top_items :
                msg += str(item) + "\n"
            msg = msg.format(message)
        elif split[1] == "player" :
            top_players = controller.top_players(10)
            msg = ""
            for player in top_players :
                msg += gachapy.objects.player_str_net_worth(player) + "\n"
            msg = msg.format(message)
        else :
            msg = "Usage: !top <item/player>"
        await message.channel.send(msg)

    if message.content.startswith("!inventory") or message.content.startswith("!inv"):
        player = controller.find_player(message.author.name + "#" + message.author.discriminator)
        msg = str(player)
        await message.channel.send(msg)
    
    await check_user(message.author)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(save())
client.loop.create_task(create_gachas())
client.run(TOKEN)