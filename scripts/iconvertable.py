from typing import Callable, List


class IConvertable:
    conversion_progress_callbacks: List[Callable] = []
    conversion_complete_callbacks: List[Callable] = []
    
    def convert(self):
        pass
    
    def add_conversion_progress_callback(self, callback: Callable):
        self.conversion_progress_callbacks.append(callback)
        
    def add_conversion_complete_callback(self, callback: Callable):
        self.conversion_complete_callbacks.append(callback)
    
    def __on_conversion_progress(self, progress: float):
        for callback in self.conversion_progress_callbacks:
            callback(progress)
    
    def __on_conversion_complete(self):
        for callback in self.conversion_complete_callbacks:
            callback()