from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from scripts.data_classes import *
from scripts.text_formatter import *
import colorlog


logger = colorlog.getLogger(__name__)


class MP3Renamer:
    purification_modes = {
        PurificationMode.splitBySymbol:
            lambda title, params:
            split_by_symbol(title, params.split_symbol, params.split_index),
        PurificationMode.sliceOffEnds:
            lambda title, params:
            split_by_symbol(title, params.left_end, params.right_end)
    }

    def apply_tags_to_song_files(self, files: list, directory: str, tags: dict):
        """Set MP3 <tags> of the songs in a list of <files> from a <directory>."""
        for file in files:
            self.set_song_tags(f"{directory}/{file}", tags[file])
            logger.info(f"Applied tags to <{file}>")

    def get_song_tags(self, files, default_tags, purification_params):
        """Returns a dictionary, where the keys are song file names and the items
        are <default_tags> with song titles generated from <files> using <purification_params>"""
        tags = {}
        for name, extension in files:
            default_tags.title = self.purify_song_title(name, purification_params)
            tags[f"{name}{extension}"] = default_tags
        logger.debug(tags)
        return tags

    def purify_song_title(self, title, params):
        return self.purification_modes.get(params.mode)(title, params).title()

    def set_song_tags(self, path: str, tags: SongTags):
        """Set MP3 <tags> of a song at <path>."""
        song = MP3(path, ID3=EasyID3)
        song.update(vars(tags))
        song.save()
