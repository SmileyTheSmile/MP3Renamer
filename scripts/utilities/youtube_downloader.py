from pytube import YouTube, Playlist, extract
from typing import List
from threading import Thread
from queue import Queue, deque
import sys
import pytube
import time

pytube.request.default_range_size = int(9437184 / 9)  # 1MB chunk size

#TODO Use Dependency injection on downloaders and video objects
class PytubeYoutubeDownloader:
    videos: Queue = Queue()
    downloading: bool = False

    def get_video(self, link: str):
        try:
            video = YouTube(link)
        except Exception as error:
            video = None
            print(f"Error while connecting: {error}")

        return video

    def add(self, video: YouTube):
        self.videos.put(video)
        
    def start_download_queue(self):
        self.downloading = True
        theads_num = min(50, self.videos.qsize())

        for _ in range(theads_num):
            worker = Thread(target=self.download_queue)
            worker.setDaemon(True)
            worker.start()

        self.videos.join()
            
    def download_queue(self):
        while not self.videos.empty():
            self.download(self.videos.get())
        self.downloading = False

    def download(self, video: YouTube):
        try:
            video.streams.get_highest_resolution().download()
            print("Download is completed successfully")
        except Exception as error:
            print(f"Error while downloading: {type(error)}")
