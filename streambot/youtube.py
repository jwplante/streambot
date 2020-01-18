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

print(getTitlesForSearchString("we are number one"))