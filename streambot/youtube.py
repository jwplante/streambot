import ast
from youtube_search import YoutubeSearch
from video import Video
import random

playlist_token = "&list="

def getLinksForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=15).to_json()
    results = ast.literal_eval(results)['videos']
    arr = []
    for res in results:
        if (playlist_token not in res['link']): 
            arr.append('https://www.youtube.com' + res['link'])

    return arr

def getTitlesForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=15).to_json()
    results = ast.literal_eval(results)['videos']
    finalString = ""
    index = 0
    for res in results:
        if (playlist_token not in res['link']): 
            finalString += str(index + 1) + '. ' + res['title'] + '\n'
            index += 1

    if finalString == "": finalString = "No videos found for the first fifteen results." 
    return finalString

def getAllVideosFromSearch(searchString, votingTag):
    results = YoutubeSearch(searchString, max_results=15).to_json()
    results = ast.literal_eval(results)['videos']
    arr = []
    for res in results:
        if (playlist_token not in res['link']): 
            arr.append(Video(res['title'], 'https://www.youtube.com' + res['link'], votingTag))
        
    return arr

def printVideoList(videos):
    string = "Results:\n"
    for video in videos:
        string += str(video) + "\n"
    return string