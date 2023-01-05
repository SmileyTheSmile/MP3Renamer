from enum import Enum
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from os.path import splitext
from os import rename
from support_funcs import *


class PurificationMode(Enum):
    """Set the way in which the clutter is removed from the song titles."""
    none = 0
    splitBySymbol = 1
    removeSymbolsAtIndexes = 2
    sliceOffEnds = 3


class MP3Renamer:
    def purify_song_title(self, song_title, purification_params):
        if purification_params["purification_mode"] == PurificationMode.splitBySymbol:
            song_title = self.__split_by_symbol__(song_title, purification_params)

        elif purification_params["purification_mode"] == PurificationMode.removeSymbolsAtIndexes:
            song_title = self.__remove_symbols_at_indexes__(
                song_title, purification_params)

        elif purification_params["purification_mode"] == PurificationMode.sliceOffEnds:
            song_title = self.slice_off_ends(song_title, purification_params)

        return song_title

    def __split_by_symbol__(self, song_title, purification_params):
        return song_title.split(purification_params["split_symbol"])[purification_params["split_index"]]

    def __remove_symbols_at_indexes__(self, song_title, purification_params):
        for i in purification_params["clutter_indexes"]:
            song_title[i] = ''
        return song_title

    def slice_off_ends(self, song_title, purification_params):
        return song_title.split()[purification_params["left_end"]: purification_params["right_end"]]

    def apply_params_to_songs(self, song_files, params):
        """Set MP3 parameters of the songs in a list."""
        for file in song_files:
            song_title, file_extension = splitext(file)
            if file_extension in params["file_params"]["supported_extensions"]:
                params["song_params"]["filename"] = file
                params["song_params"]["title"] = capitalize_all_words(
                    self.purify_song_title(song_title, params["purification_params"]))

                self.set_song_params(params["song_params"])

                if params["file_params"]["rename_files"]:
                    rename(params["song_params"]["filename"],
                           params["song_params"]["title"] + file_extension)

    def set_song_params(self, params):
        """Set MP3 parameters of a song."""
        song = MP3(params["filename"], ID3=EasyID3)

        try:
            song["title"] = params["title"]
        except:
            song["title"] = ""

        try:
            song["artist"] = params["artist"]
        except:
            song["artist"] = ""

        try:
            song["album"] = params["album"]
        except:
            song["album"] = ""

        try:
            song["date"] = params["date"]
        except:
            song["date"] = ""

        try:
            song["genre"] = params["genre"]
        except:
            song["genre"] = ""

        try:
            song["albumartist"] = params["albumartist"]
        except:
            song["albumartist"] = ""

        try:
            song["tracknumber"] = params["tracknumber"]
        except:
            song["tracknumber"] = ""

        song.save()
