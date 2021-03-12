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
    if user.bot :
        return
    if user.nick == None :
        nick = user.name
    else :
        nick = user.nick
    name = nick + " (" + user.name + "#" + user.discriminator + ")"
    id = str(user.id)
    user_item = controller.find_item_by_id(id)
    if user_item == None :
        controller.add_new_item(name,id,1)
    else :
        user_item.name = name
        user_item.rarity += 1
    user_player = controller.find_player_by_id(id)
    if user_player == None :
        controller.add_new_player(name,id,100)
    else :
        user_player.name = name
        #top_player = controller.top_players(2)[0]
        #top_item = controller.top_items(2)[0]
        #controller.change_money_player(str(user.id),top_player.get_net_worth() / top_item.rarity)

async def passive_income() :
    while True :
        top_player_list = controller.top_players(len(controller.players) + 1)
        top_item_list = controller.top_items(len(controller.items) + 1)
        top_player = top_player_list[0]
        top_item = top_item_list[0]
        average_rarity = sum([i.rarity * (top_item_list.index(i) / len(top_item_list)) for i in controller.items]) / len(controller.items)
        #delta_amount = (top_player.get_net_worth() - 10 * top_item.rarity) / len(top_player.items)
        [controller.change_money_player(i.id,average_rarity) for i in controller.players]
        await asyncio.sleep(5)

async def load_users(user) :
    if user.bot :
        return
    try :
        if user.nick == None :
            nick = user.name
        else :
            nick = user.nick
    except :
        nick = user.name
    name = nick + " (" + user.name + "#" + user.discriminator + ")"
    id = str(user.id)
    user_item = controller.find_item_by_id(id)
    if user_item == None :
        controller.add_new_item(name,id,1)
    else :
        user_item.name = name
    user_player = controller.find_player_by_id(id)
    if user_player == None :
        controller.add_new_player(name,id,100)
    else :
        user_player.name = name

@client.event
async def on_message(message): 
    if message.author == client.user:
        return
    
    # await load_users(message.author)
    await check_user(message.author)

    if message.content.startswith("!help") :
        msg = """{0.author.mention} COMMANDS:
        !info
        !pull / !p / !roll
        !inventory / !inv
        !banners / !b
        !top / !t
        !search / !s
        !rank
        """.format(message)
        await message.channel.send(msg)

    if message.content.startswith("!info") :
        msg = """{0.author.mention} INFO:
        Money is gained passively every 5 seconds. Sending more messages will NOT give you more money. Just sit and wait.
        Rarity (for the item modeled after you) is gained by sending messages. Note that rarity of items is not the same as money.
        Use !banners to see the current banners and !pull to pull an item from one.
        Banners refresh every 10 mins. Banners are randomly created.
        When you speak in any channel JayJay can see, JayJay creates a gacha account for you, which contains 100 money and no items.
        He also creates an item modeled after you. Note that your account and item are separate things. You can own your own item if you pull it.
        """.format(message)
        await message.channel.send(msg)

    if message.content.startswith("!pull") or message.content.startswith("!p") or message.content.startswith("!roll") :
        msg = "{0.author.mention} "
        split = message.content.split(' ')
        if len(split) < 2 :
            msg += "Usage: !pull <name of banner> [# of pulls]"
        else :
            if len(split) < 3 :
                count = 1
            else :
                count = int(split[2])
                if count > 20 :
                    msg += "Too many rolls, max is 20\n"
                    count = 20
            for i in range(count) :
                try :
                    item = controller.pull(str(message.author.id),split[1])
                    if item == None :
                        msg += "You do not have enough money to pull from this banner\n"
                        msg = msg.format(message)
                        await message.channel.send(msg)
                        return
                    else :
                        msg += "You pulled:\n" + str(item) + "\n"
                except gachapy.controller.PullError as e:
                    msg += str(e) + "\n"
                    msg = msg.format(message)
                    await message.channel.send(msg)
                    return
        msg = msg.format(message)
        await message.channel.send(msg)

    if message.content.startswith("!search") or message.content.startswith("!s") :
        msg = "{0.author.mention} "
        split = message.content.split(' ')
        if len(split) < 3 :
            msg += "Usage: !search <item/banner/player> <name>"
        elif split[1] == "item" :
            item = controller.find_item_by_id(split[2])
            if item == None :
                msg += "Item not found"
            else :
                msg += str(item)
        elif split[1] == "banner" :
            banner = controller.find_banner_by_name(split[2])
            if banner == None :
                msg += "Banner not found"
            else :
                msg += str(banner)
        elif split[1] == "player" :
            player = controller.find_player_by_id(split[2])
            if player == None :
                msg += "Item not found"
            else :
                msg += str(player)
        else :
            msg += "Usage: !search <item/banner/player> <name>"
        
        msg = msg.format(message)
        await message.channel.send(msg)
        
    if message.content.startswith("!banners") or message.content.startswith("!b"):
        msg = "{0.author.mention} "
        for banner in controller.banners :
            msg += str(banner) + "\n"
            msg += "\n"
        
        msg = msg.format(message)
        await message.channel.send(msg)
    
    if message.content.startswith("!top") or message.content.startswith("!t"):
        msg = "{0.author.mention} "
        split = message.content.split(' ')
        if len(split) < 2 :
            msg += "Usage: !top <item/player>"
        elif split[1] == "item" :
            msg += "Top 10 Rarest Items:\n"
            top_items = controller.top_items(10)
            for item in top_items :
                msg += str(item) + "\n"
        elif split[1] == "player" :
            msg += "Top 10 Most Valuable Players:\n"
            top_players = controller.top_players(10)
            for player in top_players :
                msg += gachapy.objects.player_str_net_worth(player) + "\n"
        else :
            msg += "Usage: !top <item/player>"
        
        msg = msg.format(message)
        await message.channel.send(msg)

    if message.content.startswith("!inventory") or message.content.startswith("!inv") :
        player = controller.find_player_by_id(str(message.author.id))
        msg = "{0.author.mention} "
        msg += str(player)
        msg = msg.format(message)
        await message.channel.send(msg)

    if message.content.startswith("!rank") :
        top_players = controller.top_players(len(controller.players))
        player = controller.find_player_by_id(str(message.author.id))
        place = top_players.index(player) + 1
        msg = "{0.author.mention} "
        msg += "Rank: " + str(place)
        msg = msg.format(message)
        await message.channel.send(msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(save())
client.loop.create_task(create_gachas())
client.loop.create_task(passive_income())
client.run(TOKEN)