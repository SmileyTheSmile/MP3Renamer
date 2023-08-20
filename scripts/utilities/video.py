from pytube import YouTube, Playlist, extract


class Video:
    download_object: YouTube
    
    def __init__(self, link: str):
        try:
            self.download_object = YouTube(link)
        except Exception as error:
            self.download_object = None
            print(f"Error while connecting: {error}")
    
    def download(self):
        try:
            self.download_object.streams.get_highest_resolution().download(
                output_path="/home/dannyboy/Documents/Projects/MP3Renamer/downloads",
                #filename="",
            )
            print("Download is completed successfully")
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(f"Error while downloading: {type(error)}")