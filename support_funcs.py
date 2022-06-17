from enum import Enum
from os import listdir, rename
from pathlib import Path
from os.path import isfile, splitext, join
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class PurificationMode(Enum):
    """Set the way in which the clutter is removed from a song title."""
    none = 0
    splitBySymbol = 1
    removeSymbolsAtIndexes = 2
    sliceOffEnds = 3


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


def get_files_from_directory(directory, supported_extensions=None, check_if_valid=True):
    directory = Path(directory).resolve()
    files = listdir(directory)
    
    if check_if_valid:
        files = get_valid_files(files, directory)
    if supported_extensions != None:
        files = get_supported_files(files, supported_extensions)
        
    return files


def get_valid_files(files, song_directory):
    """Check if the strings in a list are files in a given directory."""
    return [file for file in files if isfile(join(song_directory, file))]


def get_supported_files(files, supported_extensions):
    """Check if the extensions of the files in a list are supported."""
    return [file for file in files if splitext(file)[1] in supported_extensions]


def apply_params_to_songs(song_files, params):
    """Set MP3 parameters of the songs in a list."""
    for file in song_files:
        song_title, file_extension = splitext(file)
        if file_extension in params["file_params"]["supported_extensions"]:
            params["song_params"]["filename"] = file
            params["song_params"]["title"] = capitalize_all_words(purify_song_title(song_title, params["purification_params"]))

            set_song_params(params["song_params"])

            if params["file_params"]["rename_files"]:
                rename(params["song_params"]["filename"],
                        params["song_params"]["title"] + file_extension)


def capitalize_all_words(string):
    """Capitalizes every word in a string."""
    string = string.split()
    for i in range(len(string)):
        string[i] = string[i][0].upper() + string[i][1:]
    return ' '.join(string)


def set_song_params(params):
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