from typing import Callable, List


class IDownloadable:
    download_progress_callbacks: List[Callable] = []
    download_complete_callbacks: List[Callable] = []
    
    def connect(self, url: str):
        pass
    
    def download(self):
        pass
    
    def add_download_progress_callback(self, callback: Callable):
        self.download_progress_callbacks.append(callback)
        
    def add_download_complete_callback(self, callback: Callable):
        self.download_complete_callbacks.append(callback)
    
    def _on_download_progress(self, *args, **kwargs):
        for callback in self.download_progress_callbacks:
            callback(*args, **kwargs)
    
    def _on_download_complete(self, *args, **kwargs):
        for callback in self.download_complete_callbacks:
            callback(*args, **kwargs)