import tempfile
import threading
import ffmpeg


class ProgressFfmpeg(threading.Thread):
    """
    Credit to TomRaz: https://github.com/kkroening/ffmpeg-python/issues/43#issuecomment-1336366938
    
    This object returns progress of ffmpeg commands.
    """
    def __init__(self, vid_duration_seconds, progress_update_callback):
        threading.Thread.__init__(self, name='ProgressFfmpeg')
        self.stop_event = threading.Event()
        self.output_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.vid_duration_seconds = vid_duration_seconds
        self.progress_update_callback = progress_update_callback

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            latest_progress = self.get_latest_ms_progress()
            if latest_progress is not None:
                completed_percent = latest_progress / self.vid_duration_seconds
                self.progress_update_callback(completed_percent)

    def get_latest_ms_progress(self):
        lines = self.output_file.readlines()
        if not lines:
            return None
        
        for line in lines:
            if 'out_time_ms' in line:
                out_time_ms = line.split('=')[1]
                return int(out_time_ms) / 1000000.0


def metadata_factory(metadata: dict):
    return {
        f'metadata:g:{i}': f"{key}={value}"
        for i, (key, value) in enumerate(metadata.items())
    }

def on_update_example(progress: float):
    print(progress)
    
def convert_to_audio(in_filename: str,
                    out_filename: str,
                    metadata: dict):
    try:
        total_video_duration = float(ffmpeg.probe(in_filename)['format']['duration'])
        with ProgressFfmpeg(total_video_duration, on_update_example) as progress:
            video = ffmpeg.input(in_filename)
            stream = ffmpeg.output(
                video.audio,
                filename=out_filename,
                **metadata_factory(metadata),
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



in_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4"
out_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/1.mp3"
metadata = {
    "title": "sdf",
    "artist": "202sdgs3",
    "album": "wedgw",
    "year": "2023",
}

convert_to_audio(in_filename, out_filename, metadata)