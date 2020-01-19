import discord
import copy
import video
from youtube import getTitlesForSearchString
from youtube import getAllVideosFromSearch
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio

# client = discord.Client()
client = commands.Bot(command_prefix="!")

from queue import PriorityQueue
from heapq import heappush, heappop, heapify

votingTag = 0

heap = []
heapify(heap)
userVoteMap = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def hello(ctx):
    print("HELLO!")
    await ctx.send('Hello')

@client.command()
async def ytsearch(ctx, phrase):
    await ctx.send(getTitlesForSearchString(phrase))

@client.command()
async def add(ctx, numberResult, searchPhrase):
    global heap
    global votingTag
    # Should be in format of !add2q $numberResult $searchPhrase
    # E.g. !add2q 1 who are you 
    await ctx.send("Adding " + searchPhrase + " to the queue with voting tag #" + str(votingTag) + ".")
    vid = getAllVideosFromSearch(searchPhrase, votingTag)[0]
    heappush(heap, (vid.num_votes(), vid))
    votingTag += 1

@client.command()
async def show(ctx):
    finalStr = ""
    temp = copy.deepcopy(heap)
    tmpArr = []
    while len(temp) != 0:
        tmpArr.append(heappop(temp))

    tmpArr.reverse()
    for item in tmpArr:
        finalStr += str(item[0]) + " votes: " + item[1].video_name + " " + " with voting tag #" + str(item[1].id) + '\n'
    await ctx.send(finalStr)

@client.command()
async def upvote(ctx, votedTag):
    await abstract_vote("U", str(ctx.author), votedTag, ctx)

@client.command()
async def downvote(ctx, votedTag):
    await abstract_vote("D", str(ctx.author), votedTag, ctx)

@client.command()
async def remvote(ctx, votedTag):
    await abstract_vote("R", str(ctx.author), votedTag, ctx)

#Pass in U for upvote, R for remove, and D for downvote
async def abstract_vote(typeOfVote, username, votedTag, context):
    global heap
    temp = copy.deepcopy(heap)
    matchedItem = ""
    tempHeap = []

    for item in temp:
        currentVotingTag = item[1].id
        currentVideo = item[1]
        if int(currentVotingTag) == int(votedTag):
            if typeOfVote == "U":
                currentVideo.upvote(username)
                await context.send(username + " upvoted: " + currentVideo.video_name + ", which is now at " + str(currentVideo.num_votes()) + " votes.")
            elif typeOfVote == "D":
                currentVideo.downvote(username)
                await context.send(username + " downvoted: " + currentVideo.video_name + ", which is now at " + str(currentVideo.num_votes()) + " votes.")
            else:
                currentVideo.remove_vote(username)
                await context.send(username + " removed their vote from: " + currentVideo.video_name + ", which is now at " + str(currentVideo.num_votes()) + " votes.")

            heappush(tempHeap, (currentVideo.num_votes(), currentVideo))
        else:
            heappush(tempHeap, item)
    heap = tempHeap

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()