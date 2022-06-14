from enum import Enum
from os.path import isfile, splitext, join
from os import listdir, rename
from pathlib import Path
from music import *


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
    return get_valid_files(files, song_directory)


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


def capitalize_all_words(song_name):
    song_name = song_name.split()
    for i in range(len(song_name)):
        song_name[i] = song_name[i][0].upper() + song_name[i][1:]
    return ' '.join(song_name)


class PurificationMode(Enum):
    none = 0
    splitBySymbol = 1
    removeSymbolsAtIndexes = 2
    sliceOffEnds = 3
