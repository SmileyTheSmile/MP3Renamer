from support_funcs import *
from ui_factory import UIFactory
from mp3_renamer import PurificationMode
from os import getcwd

        
FONT = ("Arial Bold", 12)


def get_params_from_UI():
    song_dir_name = "E:\My Stuff\My Programs\MP3Renamer\songs"
    supported_extensions = [".mp3"]
    rename_files = False

    artist = "Kensuke Ushio"
    album = "Chainsaw Man Season 1"
    date = "2022"
    genre = "Indie"
    albumartist = None
    tracknum = None

    purification_mode = PurificationMode.splitBySymbol
    split_symbol = " - "
    split_index = 2
    clutter_indexes = None
    left_end = None
    right_end = None

    params = {
        "file_params": {
            "song_directory": song_dir_name,
            "supported_extensions": supported_extensions,
            "rename_files": rename_files,
        },
        "song_params": {
            "artist": artist,
            "album": album,
            "date": date,
            "genre": genre,
            "albumartist": albumartist,
            "tracknumber": tracknum
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

class Window:
    rename_files_bool = False
    selected_purification_mode = PurificationMode.none
    
    def __init__(self, name, resolution, resizable):
        self.name = name
        self.resolution = resolution
        
        ui_factory = UIFactory()
        self.window = ui_factory.window(name, resolution, resizable)
        self.toolbar = ui_factory.toolbar(self.window)
        
        self.window.config(menu=self.toolbar)
        
    def start(self):
        self._setup_layout()
        self.window.mainloop()
        
    def _setup_values(self):
        ui_factory = UIFactory()
        
        self.selected_purification_mode = ui_factory.int_var(0)
        self.rename_files_bool = ui_factory.bool_var(True)
    
    def _setup_layout(self):
        ui_factory = UIFactory()
        
        file_location_pos = 0
        artist_pos = 1
        album_pos = 2
        year_pos = 3
        genre_pos = 4
        purification_mode_pos = 5
        start_button_pos = 6
        

        self.song_dir_input = ui_factory.input_box((1, file_location_pos), True, 50, getcwd())
        self.genre_input = ui_factory.input_box((1, genre_pos), True, 50)
        self.artist_input = ui_factory.input_box((1, artist_pos), True, 50)
        self.album_input = ui_factory.input_box((1, album_pos), True, 50)
        self.year_input = ui_factory.input_box((1, year_pos), True, 50)
        
        self.song_dir_desc = ui_factory.label((0, file_location_pos), True,
                                            "Enter the song folder location",
                                            FONT,
                                            25)
        self.artist_desc = ui_factory.label((0, artist_pos), True,
                                            "Enter the all the album artists",
                                            FONT,
                                            25)
        self.album_desc = ui_factory.label((0, album_pos), True,
                                            "Enter the all the album names",
                                            FONT,
                                            25)
        self.year_desc = ui_factory.label((0, year_pos), True,
                                            "Enter the all the album years",
                                            FONT,
                                            25)
        self.genre_desc = ui_factory.label((0, genre_pos), True,
                                            "Enter the all the album genres",
                                            FONT,
                                            25)
        
        self.rename_files_check = ui_factory.check_button((2, file_location_pos), True,
                                                        "Rename files to their generated titles",
                                                        self.rename_files_bool)

        self.split_by_symbol_radio = ui_factory.radio_button((0, purification_mode_pos), True,
                                                "Separate the junk with a symbol",
                                                PurificationMode.splitBySymbol, 
                                                self._enable_purification_menu_1,
                                                self.selected_purification_mode)
        self.remove_symbols_at_indexes_radio = ui_factory.radio_button((1, purification_mode_pos), True,
                                                "Remove junk words by index",
                                                PurificationMode.removeSymbolsAtIndexes,
                                                self.selected_purification_mode)
        self.slice_off_ends_radio = ui_factory.radio_button((2, purification_mode_pos), True,
                                                "Slice off words from both ends",
                                                PurificationMode.sliceOffEnds,
                                                self.selected_purification_mode)
        
        self.start_button = ui_factory.button((0, start_button_pos), True,
                                                "Rename files", 
                                                self._finish_input)

    def _enable_purification_menu_1(self):
        pass

    def _finish_input(self):
        pass