import discord

client = discord.Client()

from queue import PriorityQueue

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
        await message.channel.send("Adding " + searchPhrase + " to the queue.")
        q.put((0, searchPhrase))
    elif message.content.startswith('!showq'):
        finalStr = ""
        temp = list(q.queue)
        for item in temp:
            finalStr += item[1] + '\n'
        await message.channel.send(finalStr)

tokenFile = open("token.txt","r+")
token = tokenFile.read()
client.run(token)
tokenFile.close()