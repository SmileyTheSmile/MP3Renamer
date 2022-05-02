import tkinter
from support_funcs import PurificationMode


def get_params_from_UI():
    song_dir_name = "E:\My Stuff\My Programs\MP3Renamer\songs"
    rename_files = True
    
    artist = "Joe Hisaishi"
    artist = "John Williams"
    album = "Howl's Moving Castle"
    year = "2004"
    genre = "Orchestral"
    album_artist = None
    album_artist = None
    track_num = None
    
    purification_mode = PurificationMode.slice_off_ends
    split_symbol = None
    split_index = None
    clutter_indexes = None
    left_end = 1
    right_end = None
    
    params = {
        "song_dir_name": song_dir_name,
        "rename_files": rename_files,
        "song_params": {
            "artist": artist,
            "album": album,
            "year": year,
            "genre": genre,
            "album_artist": album_artist,
            "track_num": track_num
        },
        "purification_params": {
            "purification_mode": purification_mode,
            "split_symbol": split_symbol,
            "split_index": split_index,
            "clutter_indexes": clutter_indexes,
            "left_end": left_end,
            "right_end": right_end
        }
    }
    
    return params