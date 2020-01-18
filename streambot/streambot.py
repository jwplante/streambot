import discord
from copy import deepcopy
import video
from youtube import getTitlesForSearchString
from youtube import getAllVideosFromSearch

client = discord.Client()

from queue import PriorityQueue

votingTag = 0

q = PriorityQueue()
userVoteMap = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global q
    global votingTag

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('!ytsearch'):
        await message.channel.send(getTitlesForSearchString(str(message.content.split("!ytsearch ")[1:])))
    elif message.content.startswith("!add2q"):
        # Should be in format of !add2q $numberResult $searchPhrase
        # E.g. !add2q 1 who are you 
        args = message.content.split(" ")[1:]
        numberResult = args[0]
        searchPhrase = " ".join(args[1:])
        await message.channel.send("Adding " + searchPhrase + " to the queue with voting tag #" + str(votingTag) + ".")
        vid = getAllVideosFromSearch(searchPhrase)[0]
        q.put((vid.num_votes(), vid, votingTag))
        votingTag += 1
    elif message.content.startswith('!showq'):
        finalStr = ""
        temp = list(q.queue)
        for item in temp:
            finalStr += item[1].video_name + ": " + str(item[0]) + " votes with voting tag #" + str(item[2]) + '\n'
        await message.channel.send(finalStr)
    elif message.content.startswith('!upvote'):
        votedTag = message.content.split(" ")[1]
        temp = list(q.queue)
        matchedItem = ""
        tempPQ = PriorityQueue()

        for item in temp:
            currentVotingTag = item[2]
            currentVideo = item[1]
            print(currentVotingTag == votedTag)
            if int(currentVotingTag) == int(votedTag) and not currentVideo.already_voted(str(message.author)):
                currentVideo.upvote(str(message.author))
                print(currentVideo.num_votes())
                tempPQ.put((currentVideo.num_votes(), currentVideo, currentVotingTag))
            else:
                tempPQ.put(item)
        q = tempPQ

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()