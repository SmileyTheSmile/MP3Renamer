from ui import *
from support_funcs import *
from os import chdir

def main():
    #main_window = Window("MP3Renamer", '800x200')
    
    #main_window.start()
    
    params = get_params_from_UI()

    chdir(params["file_params"]["song_directory"])
    
    files = get_song_files_from_directory(params["file_params"])
    
    apply_params_to_songs(files, params)
    
main()