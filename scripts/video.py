import pytube
from typing import Callable, List
from urllib.error import URLError

from scripts.video_converter import VideoConverter
from scripts.iconvertable import IConvertable
from scripts.idownloadable import IDownloadable

pytube.request.default_range_size = int(9437184 / 9)  # 1MB chunk size

class Video(IConvertable, IDownloadable):
    download_object: pytube.YouTube
    
    filepath: str = ""
    filename: str = ""
    title: str = ""
    watch_url: str = ""
    embed_url: str = ""
    thumbnail_url: str = ""
    length_sec: int = 0
    audio_extensions: List = []
    video_extensions: List = []
    
    @property
    def formatted_length(self) -> str:
        minutes_total, seconds = divmod(self.length_sec, 60)
        hours, minutes = divmod(minutes_total, 60)
        return f"{hours}:{minutes}:{seconds}"
    
    @property
    def formatted_filesize(self) -> str:
        return "0.0 MB"
    
    @property
    def formatted_current_download_speed(self) -> str:
        return "0.0 Mb/sec"
    
    @property
    def available_extensions(self) -> List[str]:
        return self.audio_extensions + self.video_extensions
            
    def connect(self, url: str):
        try:
            self.download_object = pytube.YouTube(
                url=url,
                on_complete_callback=self._on_download_complete,
                on_progress_callback=self._on_download_progress,
            )  
            self.__set_attributes()
            return True
        except URLError as error:
            print(f"Connection error: {error}")
        except Exception as error:
            print(error)
        return False
    
    def download(self):
        try:
            self.download_object.streams.get_highest_resolution().download(
                output_path=self.filepath,
                filename=self.filename,
            )
            return True
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(f"Error while downloading: {type(error)}")
        return False
    
    def __set_attributes(self):
        self.title = self.download_object.title
        self.watch_url = self.download_object.watch_url
        self.embed_url = self.download_object.embed_url
        self.thumbnail_url = self.download_object.thumbnail_url
        self.length_sec = self.download_object.length
        self.audio_extensions = ["mp3"]
        self.video_extensions = ["mp4"]