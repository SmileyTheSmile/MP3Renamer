from enum import Enum
from os.path import isfile, splitext, join
from os import listdir, rename
from pathlib import Path
from music import *


SUPPORTED_EXTENTIONS = [".mp3"]


def purify_song_name(song_name, purification_params):
    if purification_params["purification_mode"] == PurificationMode.split_by_symbol:
        song_name = song_name.split(purification_params["split_symbol"])[purification_params["split_index"]].split()
        
    elif purification_params["purification_mode"] == PurificationMode.remove_clutter:
        song_name = song_name.split()
        for i in range(len(song_name)):
            if i in purification_params["clutter_indexes"]:
                song_name[i] = ''
        
    elif purification_params["purification_mode"] == PurificationMode.slice_off_ends:
        song_name = song_name.split()[purification_params["left_end"] : purification_params["right_end"]]
    
    return capitalize_all_words(song_name)


def get_files_from_directory(song_dir_name):
    song_dir = Path(song_dir_name).resolve()
    song_files = [splitext(f) for f in listdir(song_dir) if isfile(join(song_dir, f))]

    return song_files


def apply_params_to_songs(song_files, params):
    for i in song_files:
        if i[1] in SUPPORTED_EXTENTIONS:
            params["song_params"]["filename"] = ''.join(i)
            params["song_params"]["title"] = purify_song_name(i[0], params["purification_params"])

            change_song_attributes(params["song_params"])

            if params["rename_files"]:
                rename(params["song_params"]["filename"], params["song_params"]["title"] + i[1])


def capitalize_all_words(song_name):
    for i in range(len(song_name)):
        song_name[i] = song_name[i][0].upper() + song_name[i][1:]
    
    return ' '.join(song_name)

class PurificationMode(Enum):
    split_by_symbol = 1
    remove_clutter = 2
    slice_off_ends  = 3