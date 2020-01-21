import discord
import copy
import video
import youtube_dl
from youtube import getTitlesForSearchString
from youtube import getAllVideosFromSearch
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio
from queue import PriorityQueue
from heapq import heappush, heappop, heapify

client = commands.Bot(command_prefix="!")

votingTag = 0

heap = []
heapify(heap)
userVoteMap = {}
filepath = "/tmp/streambot/"

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
async def pause(ctx):
    if (ctx.voice_client.is_playing()): ctx.voice_client.pause()

@client.command()
async def resume(ctx):
    if (ctx.voice_client.is_paused()): ctx.voice_client.resume()

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

def play_local(ctx):
    asyncio.run_coroutine_threadsafe(play(ctx), client.loop)

@client.command()
async def play(ctx):
    if not ctx.voice_client.is_playing() and len(heap) != 0:
        vid = heappop(heap)[1]
        filename = filepath + vid.get_video_id() + '.webm'
        ydl_opts = {
            'format': 'bestaudio/webm',
            'download_archive': filepath + "/vidpath",
            'outtmpl': filename
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading file from {}".format(vid.url))
            ydl.download([vid.url])

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        await ctx.send("Now playing {}".format(str(vid)))
        ctx.voice_client.play(source)
    else:
        ctx.voice_client.resume()

@client.command()
async def add(ctx, numberResult, searchPhrase):
    global heap
    global votingTag
    # Should be in format of !add2q $numberResult $searchPhrase
    # E.g. !add2q 1 who are you 
    if int(numberResult) > 10 or int(numberResult) < 1:
        await ctx.send("Error the number of the result must be (1-10), found: " + numberResult)
        return

    await ctx.send("Adding " + searchPhrase + " to the queue with voting tag #" + str(votingTag) + ".")
    vid = getAllVideosFromSearch(searchPhrase, votingTag)[int(numberResult) - 1]
    heappush(heap, (vid.num_votes(), vid))
    votingTag += 1

@client.command()
async def show(ctx):
    if len(heap) == 0:
        await ctx.send("The queue is empty, add something with `!add`")
        return

    finalStr = ""
    temp = copy.deepcopy(heap)
    tmpArr = []
    while len(temp) != 0:
        tmpArr.append(heappop(temp))

    tmpArr.reverse()
    for item in tmpArr:
        finalStr += str(-item[0]) + " votes: " + item[1].video_name + " " + " with voting tag #" + str(item[1].id) + '\n'
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

@client.command()
async def skip(ctx):
    if ctx.voice_client.is_playing(): 
        ctx.voice_client.stop()
        ctx.play_local(ctx)

#Pass in U for upvote, R for remove, and D for downvote
async def abstract_vote(typeOfVote, username, votedTag, context):
    global heap
    temp = copy.deepcopy(heap)
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

            heappush(tempHeap, (-currentVideo.num_votes(), currentVideo))
        else:
            heappush(tempHeap, item)
    heap = tempHeap

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()