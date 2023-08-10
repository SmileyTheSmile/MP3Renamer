import colorlog

from scripts.utilities import mp3_renamer as mp3r
from scripts.utilities import text_formatter as tf
from scripts.utilities import youtube_downloader as yt

from scripts.model import MVCModel


logger = colorlog.getLogger(__name__)


class MVCControl:
    mvc_model: MVCModel
    
    youtube_downloader: yt.IYoutubeDownloader

    def __init__(self, model):
        self.mvc_model = model
        self.youtube_downloader = yt.PytubeYoutubeDownloader()

        self.mvc_model.load_settings()
        
    @property
    def videos_queue(self):
        return self.youtube_downloader.videos

    @property
    def settings(self):
        return self.mvc_model.settings

    def update_files(self, directory):
        self.mvc_model.update_files(directory)

    def add_youtube_video(self, link: str):
        logger.debug(link)
        self.youtube_downloader.add(link)


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