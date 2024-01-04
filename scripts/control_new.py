from queue import Queue, deque
from threading import Thread
import flet as ft

from scripts.video import VideoObject
from scripts.videos_list_item import VideosListItem

#https://www.shanelynn.ie/using-python-threading-for-multiple-results-queue/

class VideosList(ft.ListView):
    videos: Queue = Queue()
    downloading: bool = False
    max_threads = 50
    
    def add(self, video: VideoObject):
        self.controls.append(VideosListItem(video))
        self.controls.append(ft.Divider())
        
        self.videos.put(video)
        
        if not self.downloading:
            self.start_download()
        self.update()
        
    def start_download(self):
        self.downloading = True
        theads_num = min(self.max_threads, self.videos.qsize())

        for _ in range(theads_num):
            worker = Thread(target=self.download_queue)
            worker.daemon = True
            worker.start()

        self.videos.join()
            
    def download_queue(self):
        while not self.videos.empty():
            self.videos.get().download()
            self.videos.task_done()
        self.downloading = False


class VideoControl:
    videos: Queue = Queue()
    downloading: bool = False
    max_threads = 50
    
    def add(self, video: VideoObject):
        self.videos.put(video)
        
    def start_download(self):
        self.downloading = True
        theads_num = min(self.max_threads, self.videos.qsize())

        for _ in range(theads_num):
            worker = Thread(target=self.download_queue)
            worker.daemon = True
            worker.start()

        self.videos.join()
            
    def download_queue(self):
        while not self.videos.empty():
            self.videos.get().download()
            self.videos.task_done()
        self.downloading = False

