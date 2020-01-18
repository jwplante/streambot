from __future__ import unicode_literals
from tqdm import tqdm
import time
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
        self.progbar = None # Download bar

    def on_change(self, d):
        if (d['status'] == "finished"):
            print("Download for {} finished. Now calling the callback!".format(d["filename"]))
            time.sleep(0.1)
            del self.progbar
            self.callback(d)
        if (d['status'] == "downloading"):
            try:
                self.progbar.update(d["downloaded_bytes"])
                time.sleep(0.01)
            except:
                if (d.get("total_bytes") != None):
                    self.progbar = tqdm(total=d["total_bytes"])
                    self.progbar.update(d["downloaded_bytes"])
                    time.sleep(0.01)
    
    """
    Downloads the video given the URL. 
    """
    def download_video(self, url):
        ydl_opts = {
                'format': 'bestaudio/best',
                'download_archive':self.path,
                'logger': DownloadLogger(),
                'progress_hooks':[self.on_change],
                }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading file from {}".format(url))
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
            ret_arr = []
            for line in f:
                iden = line.split(" ")[1].strip(string.whitespace)
                if (iden != ""): 
                    ret_arr.append(iden)
            return ret_arr
        except:
            print("File not found!")
            return []

