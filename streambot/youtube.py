import ast
from youtube_search import YoutubeSearch

def getLinksForSearchString(searchString):
    results = YoutubeSearch(searchString, max_results=10).to_json()
    results = ast.literal_eval(results)['videos']
    arr = []
    for res in results:
        arr.append('https://youtube.com' + res['link'])

    return arr

print(getLinksForSearchString("we are number one"))