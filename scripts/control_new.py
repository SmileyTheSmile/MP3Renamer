from queue import Queue, deque
from threading import Thread

from scripts.utilities.video import Video

class VideoControl:
    videos: Queue = Queue()
    downloading: bool = False
    max_threads = 50
    
    def add(self, video: Video):
        self.videos.put(video)
        
    def start_download(self):
        self.downloading = True
        theads_num = min(self.max_threads, self.videos.qsize())

        for _ in range(theads_num):
            worker = Thread(target=self.download_queue)
            worker.setDaemon(True)
            worker.start()

        self.videos.join()
            
    def download_queue(self):
        while not self.videos.empty():
            self.download(self.videos.get())
        self.downloading = False

    def download(self, video: Video):
        try:
            video.download()
            print("Download is completed successfully")
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(f"Error while downloading: {type(error)}")
