#https://github.com/therectifier

import asyncio
import disnake
import os
import socket
import time
import urllib.request
from disnake.ext import commands
from dotenv import load_dotenv
from mcrcon import MCRcon

load_dotenv(dotenv_path=f"bot.env")
mcBot = commands.Bot(sync_commands_debug=True)
running = False
error = False

try:
    serverport = os.getenv("server-address").split(":")[1]
except IndexError:
    serverport = 25565
if os.getenv("enable-rcon") != "true":
    print("Rcon is not enabled in your server.properties file. Please change enable-rcon to true. ")
    error = True
if os.getenv("rcon.password") == "":
    print("No password was set for Rcon. Please set a password for Rcon under rcon.password")
    error = True
if error:
    time.sleep(10)
    exit(code=0)

def rcon(cmd):
    mcr = MCRcon(os.getenv("server-ip"),os.getenv("rcon.password"),port=int(os.getenv("rcon.port")))
    try:
        mcr.connect()
        resp = mcr.command(cmd)
        mcr.disconnect()
        return resp
    except ConnectionRefusedError:
        print("Rcon unsuccessful: Server in start/stop state. ")
        return ("The server is either starting up, or shutting down. Please wait a bit, and then try again. ")

def ping(ip,port):
    if not running:
        print("Ping failed: Server down. ")
        return -1
    if not rcon("list").startswith("There are"):
        print("Ping failed: Server in start/stop state. ")
        return -2
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(("127.0.0.1",port))
    except socket.gaierror:
        print("Ping failed: Address unresolvable. ")
        return -3

async def server():
    global running
    running = True
    print("Server started. ")
    proc = await asyncio.create_subprocess_shell(os.getenv("start-script"),stdout=asyncio.subprocess.PIPE) 
    while True: 
        data = await proc.stdout.readline()
        if not data:
            break
        line = data.decode('latin1').rstrip()
        print(line)
        asyncio.create_task(on_line(line))
    running = False
    print("Server stopped. ")

async def shutdown():
    print("Auto shutdown thread started. ") 
    await asyncio.sleep(300)
    while running:
        print("Attempting auto shutdown... ")
        rcon("execute unless entity @a run stop")
        await asyncio.sleep(180)

async def webhook_send(content,uname,avatar):
    for channelid in os.getenv("chat-channel-id").split(","):
        channel = mcBot.get_channel(int(channelid))
        exist = False
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.name == "MCBotChat":
                exist = True
        if not exist:
            await channel.create_webhook(name="MCBotChat")
        for webhook in webhooks:
            try:
                await webhook.send(str(content), username=uname, avatar_url=avatar)
            except disnake.errors.InvalidArgument:
                pass
            except disnake.errors.HTTPException:
                pass

async def on_line(line):
    try:
        split = line.split("<",1)[1].split("> ",1)
        await webhook_send(split[1],split[0],"https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/977e8c4f-1c99-46cd-b070-10cd97086c08/d36qrs5-017c3744-8c94-4d47-9633-d85b991bf2f7.png")
    except IndexError:
        return

@mcBot.event
async def on_ready():
    print("Logged in as {0.user}".format(mcBot))
    await mcBot.change_presence(activity=disnake.Game("/help for help"))

@mcBot.slash_command(description="Starts the server")
async def start(inter):
    await inter.response.defer()
    if running:
        await inter.edit_original_message(content="Server is already running! ")
    else:
        asyncio.create_task(server())
        await inter.edit_original_message(content="Started server. ")

@mcBot.slash_command(description="Attempts to stop the server")
async def stop(inter):
    await inter.response.defer()
    if running:
        print("Attempting manual shutdown... ")
        try:
            await inter.edit_original_message(content=rcon("execute unless entity @a run stop"))
        except disnake.errors.HTTPException:
            await inter.edit_original_message(content="Could not stop the server. ")
    else:
        await inter.edit_original_message(content="Server is already down. ")

@mcBot.slash_command(description="Gets server information")
async def info(inter):
    await inter.response.defer()
    online = ""
    if running:
        online=rcon("list")
    await inter.edit_original_message(content="Server address: `"+os.getenv("server-address")+"`. \nServer running: "+str(running)+". \n"+online)

@mcBot.slash_command(description="Checks server address")
async def ipcheck(inter):
    await inter.response.defer()
    connectcode = ping(os.getenv("server-address").split(":")[0],int(serverport))
    if connectcode == 0:
        infoout = f'''I am able to ping the server at {os.getenv("server-address")}. 
        Check that the address you set in Minecraft matches this. If it's correct, 
        check your network connection and firewall settings.
        ''' 
        await inter.edit_original_message(content=infoout)
    elif connectcode == -1:
        await inter.edit_original_message(content="The server is not running. Please start the server to check the address. ")
    elif connectcode == -2:
        await inter.edit_original_message(content="The server is either starting up, or shutting down. Please wait a bit, and then try again. ")
    else:
        extip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        connectcode = ping(extip,serverport)
        if connectcode == 0:
            await inter.edit_original_message(content="New IP: "+extip)
            if serverport == 25565:
                os.environ["server-address"] = extip
            else:
                os.environ["server-address"] = extip + ":" + serverport
        else:
            opping = ""
            for i in os.getenv("server-op").split(','):
                opping = opping + str("<@"+i+"> ")
            await inter.edit_original_message(content="I was unable to get a new working address for the server. Please ask the bot host to update the `server-address` field and restart the bot. \nAlternatively, ask "+opping+"to use the $ip-set command to update the server address. \nHowever, you may try this address: `"+extip+"`. ")

@mcBot.slash_command(description="Sends a message in the Minecraft server")
async def say(inter,message:str):
    """
    Sends a message in the Minecraft server

    Parameters
    ----------
    message: The message to be sent
    """
    await inter.response.defer(ephemeral=True)
    if not rcon("list").startswith("There are"):
        await inter.edit_original_message(content="Server is not running. ")
        return
    try:
        await inter.edit_original_message(content=rcon('tellraw @a ["{'+str(await mcBot.fetch_user(inter.author.id))+'} '+message+'"]'))
        return
    except disnake.errors.HTTPException:
        pass
    await webhook_send(message,inter.author.name,inter.author.avatar)
    await inter.edit_original_message(content="Sent! ")

@mcBot.slash_command(description="Get help on all commands")
async def help(inter):
    await inter.response.send_message("There are 5 commands that are available to use. \nTo start the server, use `/start`. \nTo get server information, use `/info`. \nTo manually stop the server, use `/stop`. This will only stop the server if no players are online. \nTo send a message in the server, use `/say <message>`. \nIf the address given in `/info` does not work, you can do `/ipcheck`. This will update the server address if the current one does not work. ")

@mcBot.slash_command(description="Executes a Minecraft command on the Minecraft server")
async def cmd(inter,command:str):
    """
    Executes a Minecraft command on the Minecraft server

    Parameters
    ----------
    command: The command to be executed
    """
    if str(inter.author.id) not in os.getenv("server-op").split(','):
        await inter.response.send_message(content="You don't have access to this command! ",ephemeral=True)
        return
    await inter.response.defer()
    if running:
        await inter.edit_original_message(content="Rcon: "+rcon(command))
    else:
        await inter.edit_original_message(content="Please start the server to execute this command. ")

@mcBot.event
async def on_message(message):
    if message.author.bot:
        return  
    if str(message.channel.id) not in os.getenv("chat-channel-id").split(","):
        return
    await message.delete()
    if not rcon("list").startswith("There are"):
        msg = await message.channel.send("Server is not running. ")
        await asyncio.sleep(5)
        await msg.delete()
        return
    try:
        msg = await message.channel.send(rcon('tellraw @a ["{'+str(await mcBot.fetch_user(message.author.id))+'} '+message.content+'"]'))
        await asyncio.sleep(5)
        await msg.delete()
        return
    except disnake.errors.HTTPException:
        pass
    await webhook_send(message.content,message.author.name,message.author.avatar)

mcBot.run(os.getenv("bot-token"))
