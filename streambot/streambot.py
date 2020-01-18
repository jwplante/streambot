import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio

# client = discord.Client()
client = commands.Bot(command_prefix="!")

from queue import PriorityQueue

q = PriorityQueue()
vc = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#     elif message.content.startswith('!ytsearch'):
#         from youtube import getTitlesForSearchString
#         await message.channel.send(getTitlesForSearchString(str(message.content.split("!ytsearch ")[1:])))
#     elif message.content.startswith("!add2q"):
#         # Should be in format of !add2q $numberResult $searchPhrase
#         # E.g. !add2q 1 who are you
#         args = message.content.split(" ")[1:]
#         numberResult = args[0]
#         searchPhrase = " ".join(args[1:])
#         await message.channel.send("Adding " + searchPhrase + " to the queue.")
#         q.put((0, searchPhrase))
#     elif message.content.startswith('!showq'):
#         finalStr = ""
#         temp = list(q.queue)
#         for item in temp:
#             finalStr += item[1] + '\n'
#         await message.channel.send(finalStr)
#     # elif message.content.startswith('!joinvoice'):
#     #     # Should be in format of !joinvoice <voice channel>
#     #     # channelName = message.content.split(" ")[1:]
#     #     # channel = discord.utils.get(server.channels, name=channelName, type="ChannelType.voice")
#     #     try:
#     #         vc = await channel
#     #         await client.join_voice_channel(channel)
#     #     except discord.ClientException:
#     #         await client.send('Already in a voice channel...')
#     #     except discord.InvalidArgument:
#     #         await client.send('This is not a voice channel...')
#     #     else:
#     #         await client.send('Ready to play audio in ' + channel)
#     #elif message.content.startswith('!leavevoice'):

@client.command()
async def hello(ctx):
    print("HELLO!")
    await ctx.send('Hello')

@client.command()
async def play_local(ctx, filename):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
    ctx.voice_client.play(source)

    await ctx.send("Now playing file {}".format(filename))

@client.command()
async def joinvc(ctx, *, channel_name: discord.VoiceChannel):
    try:
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel_name)

        await channel_name.connect()
    except:
        print("Channel not found!!!")

@client.command()
async def leavevc(ctx):
    await ctx.voice_client.disconnect()

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()