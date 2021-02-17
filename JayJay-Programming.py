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

    if message.author == client.user:  # prevents bot from replying to itself
        return


    if message.content.startswith('!help'):  # list of commands
        msg = """CURRENT COMMANDS:
!hello
!python
!java
!c
!brainfuck
!codehelp for more info""".format(message)
        await message.channel.send(msg)

    if message.content.startswith('!codehelp') :
        msg = """For all languages:
- NO FOREVER LOOPS OR INPUT FUNCTIONS! async does not respond nicely to those and will time out the bot
- NO GRAPHICS OF ANY KIND! I am running this via the command line (WSL), which does not have graphics. For some reason, it breaks the bot instead of erroring out. Go figure
- Put a space after the command (!python, !java, etc.), even if you have a new line. You will break my parsing otherwise
- Coding blocks are allowed and even encouraged as it helps with spacing and indents

For Python: 
- Indents matter. Please use code blocks if your indents are not working in plaintext or else you will get a syntax error. Your problem, not mine

For Java: 
- Your code must be a full, runnable class. It cannot be a single line. Java is not a line-by-line language like Python
- PUT A SPACE AFTER YOUR CLASS NAME. This is because of the way I create the java source files in the back end
- Put an escape character ( \ ) before every quotation mark you make. If you don't, you break my parsing and Strings will be broken in your file

For C/C++:
- See Java stuff
- Don't suck with memory allocation. Thanks

For Brainfuck:
- Have fun
        """
        await message.channel.send(msg)


    if message.content.startswith('!hello'):  # hello (used to test bot)
        msg = 'Hello {0.author.mention}'.format(message)
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
        os.system("echo \"" + clean_msg + "\" > " + class_name + ".java")
        os.system("cat " + class_name + ".java")
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

    
    

@client.event
async def on_ready():
    # message upon ready
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    msg = "!help"
    await client.change_presence(activity=discord.Game(name=msg))

client.run(TOKEN)
