from __future__ import unicode_literals
import youtube_dl
import string

class DownloadLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Downloader:
    ## Constructor
    def __init__(self, path, callback):
        self.path = path # Callback function
        self.callback = callback # Callback after download is finished
   
    def on_finished(self, d):
        if (d['status'] == "finished"):
            print("Download for {} finished. Now calling the callback!".format(d["filename"]))
            self.callback(d)

    def download_video(self, url):
        ydl_opts = {
                'format': 'bestaudio/best',
                'download_archive':self.path,
                'logger': DownloadLogger(),
                'progress_hooks':[self.on_finished],
                }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
   
    """
    Strips the ID of the YouTube video. Returns empty string if not found.
    """
    def get_video_id(self, url):
        if (url.startswith("https://www.youtube.com/watch?v=")):
            return url[32:]
        else:
            return ""

    """
    Given the filepath, list the downloaded ID'd files
    """
    def get_downloaded_urls(self):
        try:
            f = open(self.path, "r")
            retArr = []
            for line in f:
                iden = line.split(" ")[1].strip(string.whitespace)
                if (iden != ""):
                   retArr.append(iden)
            return retArr
        except:
            print("File not found!")
            return []

def callback(d):
    pass

