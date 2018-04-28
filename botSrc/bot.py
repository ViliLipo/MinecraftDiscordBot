"""
bot module runs discordbot\n
Is all fun and games
"""
# !/usr/bin/python3
import sys
sys.path.append("./")
import discord
import asyncio
from botSrc import minecraftWrapper
from botSrc.configmanager import ConfigManager
import os

# Pass the token as a enviromentvariable"
client = discord.Client()
waitTime = 15
mc = minecraftWrapper.MinecraftWrapper()
cfgman = ConfigManager()


@client.event
async def on_ready():
    """
    When the client has connected, starts minecraftserver and adds
    its input and output to asyncio eventloop
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await asyncio.gather(minecraftFunction(), mc.cliInput())


@client.event
async def on_message(message):
    """
    Messages from regular users are passed as /say commands and messages
    from administrators are passed as server commands
    """
    if(message.channel.name == "minecraft"
            and not message.author.name == client.user.name):
        if message.author.top_role.name == "Adminboi":
            await mc.serverCommand(message.author.name, message.content)
            await client.delete_message(message)
        else:
            authorName = message.author.name
            await mc.say(authorName, message.content)
            await client.delete_message(message)


async def minecraftFunction():
        """
        Find channel called minecraft and starts to feed server output
        there.
        """
        ch = False
        for ch in client.get_all_channels():
            if (ch.name == "minecraft"):
                channel = ch
        if not ch:
            print("No channel")
            return
        async for line in mc.minecraft():
            await client.send_message(channel, line)

if __name__ == '__main__':
    """
    Grab the Discord bot-user token from os enviroment variables.
    On *nix systems use $ export MINECRAFTTOKEN=<"yourtoken">
    to set it. then discord.client.run(token) is called
    """
    client.run(cfgman.getToken())
