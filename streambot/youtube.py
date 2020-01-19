import ast
from youtube_search import YoutubeSearch
from video import Video
import random

def getLinksForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=10).to_json()
    results = ast.literal_eval(results)['videos']
    arr = []
    for res in results:
        arr.append('https://www.youtube.com' + res['link'])

    return arr

def getTitlesForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=10).to_json()
    results = ast.literal_eval(results)['videos']
    finalString = ""
    for index, res in enumerate(results):
        finalString += str(index + 1) + '. ' + res['title'] + '\n'

    return finalString

def getAllVideosFromSearch(searchString, votingTag):
    results = YoutubeSearch(searchString, max_results=10).to_json()
    results = ast.literal_eval(results)['videos']
    arr = []
    for res in results:
        arr.append(Video(res['title'], 'https://www.youtube.com' + res['link'], votingTag))
        
    return arr

def printVideoList(videos):
    string = "Results:\n"
    for video in videos:
        string += str(video) + "\n"
    return string