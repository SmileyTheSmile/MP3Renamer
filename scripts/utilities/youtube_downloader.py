from pytube import YouTube, Playlist, extract
from pytube.cli import on_progress
from typing import List
import sys


#TODO Use Dependency injection on downloaders and video objects
class PytubeYoutubeDownloader:
    videos: List[YouTube] = []

    def add(self, link: str, on_progress, on_complete):
        video = YouTube(
            link,
            on_progress_callback=on_progress,
            on_complete_callback=on_complete
        )
        #video.register_on_progress_callback(show_progress_bar)
        self.videos.append(video)

    def download(self, video: YouTube):
        video.streams.get_highest_resolution().download()

    def get_link_type(self, link: str):
        print(extract.playlist_id(link))
        if extract.playlist_id(link) != "":
            result = Playlist(link)
        else:
            result = YouTube(link)
        
    def download_queue(self):
        for video in self.videos:
            try:
                video.streams.get_audio_only().download()
                print("Download is completed successfully")
            except:
                print("An error has occurred")
