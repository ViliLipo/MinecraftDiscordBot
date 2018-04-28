#!/usr/bin/python3
import discord
import asyncio
import minecraftWrapper
import os

# Pass the token as a enviromentvariable"
client = discord.Client()
waitTime = 15
mc = minecraftWrapper.MinecraftWrapper()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await asyncio.gather(minecraftFunction(), mc.cliInput())


@client.event
async def on_message(message):
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
        print("hello")
        ch = False
        for ch in client.get_all_channels():
            if (ch.name == "minecraft") :
                channel = ch
        if not ch:
            print("No channel")
            return
        async for line in mc.minecraft():
            await client.send_message(channel, line)
        # await mc.cliInput()
# print(sys.argv[1])
client.run(os.environ['MINECRAFTTOKEN'])
