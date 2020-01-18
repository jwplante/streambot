import discord
from copy import deepcopy

client = discord.Client()

from queue import PriorityQueue

votingTag = 0

q = PriorityQueue()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('!ytsearch'):
        from youtube import getTitlesForSearchString
        await message.channel.send(getTitlesForSearchString(str(message.content.split("!ytsearch ")[1:])))
    elif message.content.startswith("!add2q"):
        # Should be in format of !add2q $numberResult $searchPhrase
        # E.g. !add2q 1 who are you 
        args = message.content.split(" ")[1:]
        numberResult = args[0]
        searchPhrase = " ".join(args[1:])
        await message.channel.send("Adding " + searchPhrase + " to the queue with voting tag #" + str(votingTag) + ".")
        q.put((1, searchPhrase, votingTag))
        # votingTag += 1
    elif message.content.startswith('!showq'):
        finalStr = ""
        temp = list(q.queue)
        for item in temp:
            finalStr += item[1] + ": " + str(item[0]) + " votes with voting tag #" + str(item[2]) + '\n'
        await message.channel.send(finalStr)
    elif message.content.startswith('!vote'):
        votedTag = message.content.split(" ")[1]
        temp = list(q.queue)
        matchedItem = ""
        for item in temp:
            print(item[2], votedTag)
            if item[2] == int(votedTag):
                matchedItem = (item[0] + 1, item[1], item[2])
                q.put(matchedItem)
                pass

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()