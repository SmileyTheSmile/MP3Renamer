import colorlog

from scripts.utilities import youtube_downloader as yt

from scripts.model import MVCModel


logger = colorlog.getLogger(__name__)


class MVCControl:
    mvc_model: MVCModel
    
    youtube_downloader: yt.PytubeYoutubeDownloader

    def __init__(self, model):
        self.mvc_model = model
        self.youtube_downloader = yt.PytubeYoutubeDownloader()

        self.mvc_model.load_settings()
        
    @property
    def videos_queue(self):
        return self.youtube_downloader.videos

    def get_video(self, link: str):
        return self.youtube_downloader.get_video(link)

    def update_files(self, directory):
        self.mvc_model.update_files(directory)

    def add_youtube_video(self, link: str, on_progress, on_complete):
        logger.debug(link)
        self.youtube_downloader.add(link, on_progress, on_complete)
    
    def process_link(self, link: str):
        self.youtube_downloader.get_link_type(link)
    
    def download(self, video):
        self.youtube_downloader.add(video)
        if not self.youtube_downloader.downloading:
            self.youtube_downloader.start_download_queue()
        '''
        default_song_tags = SongTags(
            artist="Kensuke Ushio",
            album="Chainsaw Man",
            date="2022",
            genre="Indie",
            albumartist='',
            tracknumber='',
        )
        song_files = mp3r.generate_songs(files)
        song_files = f_op.group_by_extension(song_files)
        song_files = tf.apply_patterns_to_list(song_files, [r"Chainsaw Man OST - \d+ - *", ""]) #r"\.mp3"])
        song_tags = mp3r.get_song_tags(song_files, default_song_tags, purification_params)
        mp3r.apply_tags_to_song_files(song_files, file_params.directory, song_tags)
        '''