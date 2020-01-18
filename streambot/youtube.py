import ast
from youtube_search import YoutubeSearch

def getLinksForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=10).to_json()
    results = ast.literal_eval(results)['videos']
    arr = []
    for res in results:
        arr.append('https://youtube.com' + res['link'])

    return arr

def getTitlesForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=10).to_json()
    results = ast.literal_eval(results)['videos']
    finalString = ""
    for index, res in enumerate(results):
        finalString += str(index + 1) + '. ' + res['title'] + '\n'

    return finalString

# print(getTitlesForSearchString("we are number one"))
from queue import PriorityQueue
finalStr = ""
q = PriorityQueue()
q.put((0, "Who are you"))
q.put((0, "Who are me"))
temp = list(q.queue)
for item in temp:
    finalStr += item[1] + '\n'
print(finalStr)