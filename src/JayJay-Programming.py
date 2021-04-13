import discord

import sys
import io
import os
import traceback
import subprocess
import signal

script_dir = os.path.dirname(__file__)
token_path = "../lib/token.txt"
f = open(os.path.join(script_dir, token_path), "r")
TOKEN = f.read()
client = discord.Client()


class TimeOutException(Exception):
    pass


def alarm_handler(signum, frame):
    print("ALARM signal received")
    raise TimeOutException()


def search(list, elem):
    for i in range(len(list)):
        if list[i] == elem:
            return i
    return -1


@client.event
async def on_message(message):  # bulk of command handling

    if message.author == client.user:  # prevents bot from replying to itself
        return

    if message.content.startswith("!help"):  # list of commands
        msg = """CURRENT COMMANDS:
!hello
!python
!java
!c
!brainfuck
!codehelp for more info""".format(
            message
        )
        await message.channel.send(msg)

    if message.content.startswith("!codehelp"):
        msg = """For all languages:
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

    if message.content.startswith("!hello"):  # hello (used to test bot)
        msg = "Hello {0.author.mention}".format(message)
        await message.channel.send(msg)

    elif message.content.startswith("!python"):  # python interpreter
        async with message.channel.typing():  # have bot type while processing
            if (
                "import sys" in message.content
            ):  # sys not supported for safety of system
                msg = "Error: sys support is not offered".format(message)
                await message.channel.send(msg)
                return
            elif (
                "import os" in message.content
            ):  # os not supported for safety of system
                msg = "Error: os support is not offered".format(message)
                await message.channel.send(msg)
                return

            old_stdout = sys.stdout  # saving stdout pipe
            old_stderr = sys.stderr  # saving sterr pipe
            sys.stdout = (
                buffer_out
            ) = io.StringIO()  # replace stdout with new string io buffer
            sys.stderr = (
                buffer_err
            ) = io.StringIO()  # replace stderr with new string io buffer

            split = message.content.split(" ")
            if len(split) < 2:  # code not supplied, print helper message
                msg = "Usage: !python <code to run>".format(message)
                await message.channel.send(msg)
                return

            msg = " ".join(split[1:])
            clean_msg = msg.replace(
                "`", ""
            )  # clean python code from message for execution
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(3)  # create three second kill switch (prevent infinite loops)
            try:
                exec(compile(clean_msg, "text.txt", "exec"))  # attempt to run
            except TimeOutException:  # detect timeout
                msg = "Error: Bot timed out after 3 seconds".format(message)
                await message.channel.send(msg)
                return
            except:
                traceback.print_exc()  # print error to console if found
            signal.alarm(0)  # reset alarm

            out_value = buffer_out.getvalue()  # grab execution values from stdout
            err_value = buffer_err.getvalue()  # grab execution values from stderr

            sys.stdout = old_stdout  # hook up stdout with old pipe
            sys.stderr = old_stderr  # hook up stderr with old pipe

        await message.channel.send(err_value + out_value)

    elif message.content.startswith("!java"):  # java compiler
        async with message.channel.typing():
            if (
                "Scanner" in message.content
            ):  # input not supported to prevent bot crashes
                msg = "Error: Input support is not offered".format(message)
                await message.channel.send(msg)
                return

            split = message.content.split(" ")
            if len(split) < 2:  # code not supplied, print helper message
                msg = "Usage: !java <code to run>".format(message)
                await message.channel.send(msg)
                return

            msg = " ".join(split[1:])
            class_name = split[
                search(split, "class") + 1
            ]  # find class name for file name
            if class_name == "!java":  # class not specified
                msg = "Error: Class name not specified".format(message)
                await message.channel.send(msg)
                return

            clean_msg = msg.replace(
                "`", ""
            )  # clean java code from message for compilation

            os.system("rm -f *.java *.class")  # remove previosuly run java files
            os.system(
                'echo "' + clean_msg + '" > ' + class_name + ".java"
            )  # place java class into java source file
            output = ""
            output += subprocess.run(
                ["javac", class_name + ".java"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout.decode(
                "utf-8"
            )  # attempt to compile class and record results
            if output == "":
                signal.signal(signal.SIGALRM, alarm_handler)
                signal.alarm(
                    3
                )  # create three second kill switch (prevent infinite loops)
                try:
                    output += subprocess.run(
                        ["timeout", "3s", "java", class_name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    ).stdout.decode(
                        "utf-8"
                    )  # if compilation succeeded, attempt to run class and record results
                except TimeOutException:  # detect timeout
                    os.system(
                        "pkill -f java"
                    )  # kill processes in case of extra threads
                    msg = "Error: Bot timed out after 3 seconds".format(message)
                    await message.channel.send(msg)
                    return
                signal.alarm(0)  # reset alarm

        await message.channel.send(output)

    elif message.content.startswith("!c"):
        async with message.channel.typing():
            split = message.content.split(" ")
            if len(split) < 2:
                msg = "Usage: !c <code to run>".format(message)
                await message.channel.send(msg)
                return

            msg = " ".join(split[1:])
            clean_msg = msg.replace(
                "`", ""
            )  # clean c code from message for compilation

            os.system("rm -f *.c *.out")  # remove previously run c files
            os.system('echo "' + msg + '" > main.c')  # place c code into source file
            output = ""
            output += subprocess.run(
                ["gcc", "main.c"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).stdout.decode(
                "utf-8"
            )  # attempt to compile source code and record results
            if output == "":
                signal.signal(signal.SIGALRM, alarm_handler)
                signal.alarm(3)
                try:
                    output += subprocess.run(
                        ["./a.out"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    ).stdout.decode(
                        "utf-8"
                    )  # if compilation succeeded, attempt to run executable and record results
                except TimeOutException:
                    msg = "Error: Bot timed out after 3 seconds".format(message)
                    await message.channel.send(msg)
                    return
                signal.alarm(0)

        await message.channel.send(output)

    elif message.content.startswith("!brainfuck"):
        async with message.channel.typing():
            split = message.content.split(" ")
            if len(split) < 2:
                msg = "Usage: !brainfuck <code to run>".format(message)
                await message.channel.send(msg)
                return

            msg = " ".join(split[1:])
            clean_msg = msg.replace(
                "`", ""
            )  # clean bf code from message for compilation

            stream = os.popen(
                'echo "' + clean_msg + '" | brainfuck'
            )  # pipe code directly into bf interpreter
            output = stream.read()  # read output

        await message.channel.send(output)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    msg = "!help"
    await client.change_presence(activity=discord.Game(name=msg))  # set status to !help


client.run(TOKEN)
