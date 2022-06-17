from enum import Enum
from os.path import isfile, splitext, join
from os import listdir, rename
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def purify_song_title(song_title, purification_params):
    if purification_params["purification_mode"] == PurificationMode.splitBySymbol:
        song_title = split_by_symbol(song_title, purification_params)

    elif purification_params["purification_mode"] == PurificationMode.removeSymbolsAtIndexes:
        song_title = remove_symbols_at_indexes(song_title, purification_params)

    elif purification_params["purification_mode"] == PurificationMode.sliceOffEnds:
        song_title = slice_off_ends(song_title, purification_params)

    return song_title


def split_by_symbol(song_title, purification_params):
    return song_title.split(purification_params["split_symbol"])[purification_params["split_index"]].split()


def remove_symbols_at_indexes(song_title, purification_params):
    for i in purification_params["clutter_indexes"]:
        song_title[i] = ''
    return song_title


def slice_off_ends(song_title, purification_params):
    return song_title.split()[purification_params["left_end"]: purification_params["right_end"]]


def get_song_files_from_directory(file_params):
    song_directory = Path(file_params["song_directory"]).resolve()
    files = listdir(song_directory)
    return get_valid_files(files, song_directory), file_params["supported_extensions"]


def get_supported_files(files, supported_extensions):
    return [file for file in files if splitext(file)[1] in supported_extensions]


def get_valid_files(files, song_directory):
    return [file for file in files if isfile(join(song_directory, file))]


def apply_params_to_songs(song_files, params):
    for file in song_files:
        song_title, file_extension = splitext(file)
        if file_extension in params["file_params"]["supported_extensions"]:
            params["song_params"]["filename"] = file
            params["song_params"]["title"] = capitalize_all_words(purify_song_title(song_title, params["purification_params"]))

            change_song_attributes(params["song_params"])

            if params["file_params"]["rename_files"]:
                rename(params["song_params"]["filename"],
                        params["song_params"]["title"] + file_extension)


def capitalize_all_words(string):
    """Capitalizes every word in a sentence."""
        
    string = string.split()
    for i in range(len(string)):
        string[i] = "{}{}".format(string[i][0].upper(), string[i][1:])
        #string[i] = string[i][0].upper() + string[i][1:]
    return ' '.join(string)


def change_song_attributes(song_params):
    song = MP3(song_params["filename"], ID3=EasyID3)

    try:
        song["title"] = song_params["title"]
    except:
        song["title"] = ""

    try:
        song["artist"] = song_params["artist"]
    except:
        song["artist"] = ""

    try:
        song["album"] = song_params["album"]
    except:
        song["album"] = ""

    try:
        song["date"] = song_params["date"]
    except:
        song["date"] = ""

    try:
        song["genre"] = song_params["genre"]
    except:
        song["genre"] = ""

    try:
        song["albumartist"] = song_params["albumartist"]
    except:
        song["albumartist"] = ""

    try:
        song["tracknumber"] = song_params["tracknumber"]
    except:
        song["tracknumber"] = ""

    song.save()


class PurificationMode(Enum):
    none = 0
    splitBySymbol = 1
    removeSymbolsAtIndexes = 2
    sliceOffEnds = 3
