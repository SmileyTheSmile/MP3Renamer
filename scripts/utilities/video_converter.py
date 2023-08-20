import tempfile
import threading
import ffmpeg
from typing import Callable


class ProgressFfmpeg(threading.Thread):
    """
    Credit to TomRaz: https://github.com/kkroening/ffmpeg-python/issues/43#issuecomment-1336366938
    
    This object helps track the progress and completion of ffmpeg commands.
    """
    def __init__(self,
        total_duration_seconds: float,
        progress_update_callback: Callable,
        complete_update_callback: Callable
    ):
        self.total_duration_seconds = total_duration_seconds
        self.progress_update_callback = progress_update_callback
        self.complete_update_callback = complete_update_callback
        
        threading.Thread.__init__(self, name='ProgressFfmpeg')
        self.stop_event = threading.Event()
        self.output_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            latest_progress = self.get_latest_ms_progress()
            if latest_progress is not None:
                completed_percent = latest_progress / self.total_duration_seconds
                self.progress_update_callback(completed_percent)
        self.complete_update_callback()

    def get_latest_ms_progress(self):
        for line in self.output_file.readlines():
            if 'out_time_ms' in line:
                out_time_ms = line.split('=')[1]
                return int(out_time_ms) / 1000000.0
        return None

    
class VideoConverter:
    def convert_to_audio(self,
        in_filename: str,
        out_filename: str,
        metadata: dict,
        progress_callback: Callable,
        complete_callback: Callable
    ):
        try:
            total_video_duration = float(ffmpeg.probe(in_filename)['format']['duration'])
            with ProgressFfmpeg(total_video_duration, progress_callback, complete_callback) as progress:
                video = ffmpeg.input(in_filename)
                stream = ffmpeg.output(
                    video.audio,
                    out_filename,
                    **self.metadata_factory(metadata),
                ).global_args(
                    '-progress',
                    progress.output_file.name
                ).run(
                    capture_stdout=True,
                    capture_stderr=True,
                    overwrite_output=True,
                )
        except ffmpeg.Error as e:
            print(e.stderr)

    def metadata_factory(self, metadata: dict):
        return {
            f'metadata:g:{i}': f"{key}={value}"
            for i, (key, value) in enumerate(metadata.items())
        }

    
if __name__ == "__main__":
    
    def on_update_example(progress: float):
        print(progress)
        
    def on_complete_example():
        print("Complete")
        
    in_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4"
    out_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/1.mp3"
    metadata = {
        "title": "sdf",
        "artist": "202sdgs3",
        "album": "wedgw",
        "year": "2023",
    }

    VideoConverter().convert_to_audio(
        in_filename,
        out_filename,
        metadata,
        on_update_example,
        on_complete_example
    )