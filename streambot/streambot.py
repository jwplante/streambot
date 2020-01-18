import discord
from copy import deepcopy
import video
from youtube import getTitlesForSearchString
from youtube import getAllVideosFromSearch
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio

# client = discord.Client()
client = commands.Bot(command_prefix="!")

from queue import PriorityQueue

votingTag = 0

q = PriorityQueue()
userVoteMap = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     global q
#     global votingTag

#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#     elif message.content.startswith('!upvote'):
#         votedTag = message.content.split(" ")[1]
#         temp = list(q.queue)
#         matchedItem = ""
#         tempPQ = PriorityQueue()

#         for item in temp:
#             currentVotingTag = item[2]
#             currentVideo = item[1]
#             print(currentVotingTag == votedTag)
#             if int(currentVotingTag) == int(votedTag) and not currentVideo.already_voted(str(message.author)):
#                 currentVideo.upvote(str(message.author))
#                 print(currentVideo.num_votes())
#                 tempPQ.put((currentVideo.num_votes(), currentVideo, currentVotingTag))
#             else:
#                 tempPQ.put(item)
#         q = tempPQ

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
async def pause(ctx):
    if (ctx.voice.is_playing()): ctx.voice_client.pause()

@client.command()
async def resume(ctx):
    if (ctx.voice.is_paused()): ctx.voice_client.resume()

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
async def ytsearch(ctx):
    await ctx.send(getTitlesForSearchString(str(message.content.split("!ytsearch ")[1:])))

@client.command()
async def add2q(ctx, numberResult, searchPhrase):
    global q
    global votingTag
    # Should be in format of !add2q $numberResult $searchPhrase
    # E.g. !add2q 1 who are you 
    # args = message.content.split(" ")[1:]
    # numberResult = args[0]
    # searchPhrase = " ".join(args[1:])
    await ctx.send("Adding " + searchPhrase + " to the queue with voting tag #" + str(votingTag) + ".")
    vid = getAllVideosFromSearch(searchPhrase)[0]
    q.put((vid.num_votes(), vid, votingTag))
    votingTag += 1

@client.command()
async def showq(ctx):
    finalStr = ""
    temp = list(q.queue)
    for item in temp:
        finalStr += item[1].video_name + ": " + str(item[0]) + " votes with voting tag #" + str(item[2]) + '\n'
    await ctx.send(finalStr)

@client.command()
async def upvote(ctx, votedTag):
    abstract_vote("U", str(ctx.author), votedTag)

@client.command()
async def downvote(ctx, votedTag):
    print(1234)
    abstract_vote("D", str(ctx.author), votedTag)

@client.command()
async def remvote(ctx, votedTag):
    abstract_vote("R", str(ctx.author), votedTag)

#Pass in U for upvote, R for remove, and D for downvote
def abstract_vote(typeOfVote, username, votedTag):
    global q
    temp = list(q.queue)
    matchedItem = ""
    tempPQ = PriorityQueue()

    for item in temp:
        currentVotingTag = item[2]
        currentVideo = item[1]
        if int(currentVotingTag) == int(votedTag):
            if typeOfVote == "U":
                currentVideo.upvote(username)
            elif typeOfVote == "D":
                currentVideo.downvote(username)
            else:
                currentVideo.remove_vote(username)

            tempPQ.put((currentVideo.num_votes(), currentVideo, currentVotingTag))
        else:
            tempPQ.put(item)
    q = tempPQ

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()