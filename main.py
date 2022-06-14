from ui import *
from support_funcs import *
from os import chdir


def main():
    #main_window = Window("MP3Renamer", '800x200')
    
    #main_window.start()
    
    params = get_params_from_UI()
    
    song_files = get_files_from_directory(params["song_dir_name"])

    chdir(params["song_dir_name"])
    
    apply_params_to_songs(song_files, params)
    
main()