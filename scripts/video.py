import pytube
import os
from typing import Callable, List
from urllib.error import URLError
from datetime import datetime

from scripts.video_converter import VideoConverter
from scripts.iconvertable import IConvertable
from scripts.idownloadable import IDownloadable

pytube.request.default_range_size = int(9437184 / 9)  # 1MB chunk size

# TODO Separate connection object from download stream
class VideoInfo:
    download_object: pytube.YouTube

    filepath: str = None
    filename: str = None
    
    _title: str = None
    _watch_url: str = None
    _embed_url: str = None
    thumbnail_url: str = None
    length_sec: int = 0
    audio_extensions: List = []
    video_extensions: List = []
    
    filesize_bytes: int = 0

    @property
    def title(self) -> tuple:
        if not self._title:
            self._title = self.download_object.title
        return self._title

    @property
    def watch_url(self) -> tuple:
        if not self._watch_url:
            self._watch_url = self.download_object.watch_url
        return self._watch_url

    @property
    def embed_url(self) -> tuple:
        if not self._embed_url:
            self._embed_url = self.download_object.embed_url
        return self._embed_url

    @property
    def formatted_length(self) -> tuple:
        minutes_total, seconds = divmod(self.length_sec, 60)
        hours, minutes = divmod(minutes_total, 60)
        return hours, minutes, seconds

    @property
    def filesize_MB(self) -> str:
        return self.filesize_bytes / 1024

    @property
    def current_download_speed(self) -> float:
        return 0.0

    @property
    def available_extensions(self) -> List[str]:
        return self.audio_extensions + self.video_extensions

    def connect(self, url: str):
        try:
            self.download_object = pytube.YouTube(
                url=url,
            )
            self.__set_attributes()
            return True
        except URLError as error:
            print(f"Connection error: {error}")
        except Exception as error:
            print(error)
        return False

    def get_stream(self,
                 skip_existing_file: bool = True,
                 timeout_seconds: int = 60,
                 max_retries: int = 0,
                 ) -> bool:
        
        file_path = os.path.join(
            target_directory(self.filepath),
            f"{self.filename}.{self.video_extensions[0]}"
        )

        # Check if file exists
        if os.path.isfile(file_path) and skip_existing_file:
            print(f'file {file_path} already exists, skipping')
            self._on_download_complete()
            return True

        with open(file_path, "wb") as file:
            stream = self.download_object.streams.get_highest_resolution()
            url, self.filesize_bytes, bytes_downloaded = stream.url, stream.filesize, 0
            try:
                return VideoObject(url, self.filesize_bytes, bytes_downloaded)
            except Exception as error:
                print(f"Error while getting stream info: {type(error)}")
        return None

    def __set_attributes(self):
        self.title = self.download_object.title
        self.watch_url = self.download_object.watch_url
        self.embed_url = self.download_object.embed_url
        self.thumbnail_url = self.download_object.thumbnail_url
        self.length_sec = self.download_object.length
        self.audio_extensions = ["mp3"]
        self.video_extensions = ["mp4"]


class VideoObject(IConvertable, IDownloadable):
    url: str
    filepath: str
    filesize_bytes: float
    
    download_progress_callbacks: List[Callable] = []
    download_complete_callbacks: List[Callable] = []
    
    def __init__(self, url, filepath, filesize_bytes):
        self.url = url
        self.filepath = filepath
        self.filesize_bytes = filesize_bytes
    
    def _on_download_progress(self, progress_percentage):
        for callback in self.download_progress_callbacks:
            callback(progress_percentage)
    
    def _on_download_complete(self):
        for callback in self.download_complete_callbacks:
            callback()

    def download(self,
            skip_existing_file: bool = True,
            timeout_seconds: int = 60,
            max_retries: int = 0,
        ) -> bool:
        
        file_path = os.path.join(
            target_directory(self.filepath),
            f"{self.filename}.{self.video_extensions[0]}"
        )

        # Check if file exists
        if os.path.isfile(file_path) and skip_existing_file:
            print(f'file {file_path} already exists, skipping')
            self._on_download_complete()
            return True

        with open(file_path, "wb") as file:
            bytes_downloaded = 0
            download_start_time = datetime.now()
            try:
                for chunk in pytube.request.stream(
                    url=self.url,
                    timeout=timeout_seconds,
                    max_retries=max_retries
                ):
                    file.write(chunk)  
                    bytes_downloaded += len(chunk)
                    
                    time_elapsed_seconds = (datetime.now() - download_start_time).total_seconds()  
                    progress_percentage = bytes_downloaded / self.filesize_bytes
                    speed = bytes_downloaded / (1024**2 * time_elapsed_seconds)
                    seconds_left = (self.filesize_bytes - bytes_downloaded) / (1024**2 * speed)
                    
                    self._on_download_progress(
                        progress=progress_percentage,
                        speed=speed,
                        seconds_left=seconds_left,
                        time_elapsed_seconds=time_elapsed_seconds
                    )
                self._on_download_complete()
                return True
            except Exception as error:
                print(f"Error while downloading: {type(error)}")
        return False
        



def target_directory(output_path=None) -> str:
    """
    Function for determining target directory of a download.
    Returns an absolute path (if relative one given) or the current
    path (if none given). Makes directory if it does not exist.

    :type output_path: str
        :rtype: str
    :returns:
        An absolute directory path as a string.
    """
    if output_path:
        if not os.path.isabs(output_path):
            output_path = os.path.join(os.getcwd(), output_path)
    else:
        output_path = os.getcwd()
    os.makedirs(output_path, exist_ok=True)
    return output_path
