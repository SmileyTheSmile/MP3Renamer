from pytube import YouTube, Playlist, extract
from typing import Callable, List

from scripts.utilities.video_converter import VideoConverter

    
class Video:
    download_object: YouTube
    
    filepath: str
    filename: str
    
    download_progress_callbacks: List[Callable] = []
    download_complete_callbacks: List[Callable] = []
    conversion_progress_callbacks: List[Callable] = []
    conversion_complete_callbacks: List[Callable] = []
    
    def __init__(self, url: str):
        self.url = url
            
    def connect(self):
        try:
            self.download_object = YouTube(
                url=self.url,
                on_complete_callback=self.__on_download_complete,
                on_progress_callback=self.__on_download_progress,
            )   
            return True
        except Exception as error:
            return False
    
    def download(self, output_path: str, filename: str):
        self.filepath = output_path
        self.filename = filename
        try:
            self.download_object.streams.get_highest_resolution().download(
                output_path=output_path,
                filename=filename,
            )
            return True
        except Exception as error:
            return False
    
    def convert(self):
        try:
            pass
        except Exception as error:
            return False
    
    def add_download_progress_callback(self, callback: Callable):
        self.download_progress_callbacks.append(callback)
        
    def add_download_complete_callback(self, callback: Callable):
        self.download_complete_callbacks.append(callback)
    
    def __on_download_progress(self, stream, chunk, bytes_remaining):
        progress_percentage =  (stream.filesize - bytes_remaining) / stream.filesize
        for callback in self.download_progress_callbacks:
            callback(progress_percentage)
    
    def __on_download_complete(self, stream, path):
        for callback in self.download_complete_callbacks:
            callback()
    
    def __on_conversion_progress(self, progress: float):
        for callback in self.conversion_progress_callbacks:
            callback(progress)
    
    def __on_conversion_complete(self):
        for callback in self.conversion_complete_callbacks:
            callback()