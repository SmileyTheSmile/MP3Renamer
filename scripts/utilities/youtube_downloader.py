from pytube import YouTube
from typing import List

'''
>>> yt = YouTube(
        'http://youtube.com/watch?v=2lAe1cqCOXo',
        on_progress_callback=progress_func,
        on_complete_callback=complete_func,
        proxies=my_proxies,
        use_oauth=False,
        allow_oauth_cache=True
    )
'''

#TODO Use Dependency injection on downloaders and video objects
class IYoutubeDownloader:
    videos: List[YouTube] = []
    
    def add(self, link: str) -> None:
        """
        Add video to the download queue.

        Args:
            link (str): Link to the video.
        """
        pass
    
    def download_queue(self) -> None:
        """
        _summary_

        Args:
            link (str): _description_
        """
        pass

class IYoutubeVideo:
    pass

class PytubeYoutubeDownloader(IYoutubeDownloader):
    def add(self, link: str):
        self.videos.append(YouTube(link))
        
    def download_queue(self):
        for video in self.videos:
            try:
                video.streams.get_audio_only().download()
                print("Download is completed successfully")
            except:
                print("An error has occurred")


class PytubeYoutubeVideo(IYoutubeVideo, YouTube):
    @property
    def thumbnail_url(self) -> str:
        return super().thumbnail_url
