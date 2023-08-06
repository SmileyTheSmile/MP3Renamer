from pytube import YouTube

'''
>>> yt = YouTube(
        'http://youtube.com/watch?v=2lAe1cqCOXo',
        on_progress_callback=progress_func,
        on_complete_callback=complete_func,
        proxies=my_proxies,
        use_oauth=False,
        allow_oauth_cache=True
    )
'''

class IYoutubeDownloader:
    def download(link: str) -> None:
        """
        _summary_

        Args:
            link (str): _description_
        """
        pass
    
    def download_playlist(link: str) -> None:
        """
        _summary_

        Args:
            link (str): _description_
        """
        pass

class PytubeYoutubeDownloader(IYoutubeDownloader):
    def download(link: str):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_audio_only()
        print(youtubeObject.title)
        try:
            youtubeObject.download()
            print("Download is completed successfully")
        except:
            print("An error has occurred")



if __name__ == '__main__':
    PytubeYoutubeDownloader.download("https://www.youtube.com/watch?v=V-GC9LdbBRo")

    #link = input("Enter the YouTube video URL: ")
    #Download(link)