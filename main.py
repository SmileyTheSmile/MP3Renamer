from mp3_renamer import MP3Renamer
from file_operator import FileOperator
from ui import *
from support_funcs import *
from os import chdir


def main():
    #main_window = Window("MP3Renamer", '800x200', False)
    #main_window.start()
    
    params = get_params_from_UI()
    
    chdir(params["file_params"]["song_directory"])

    file_operator = FileOperator()
    song_files = file_operator.get_files_from_directory(params["file_params"]["song_directory"], params["file_params"]["supported_extensions"])

    mp3_renamer = MP3Renamer()
    mp3_renamer.apply_params_to_songs(song_files, params)


if __name__ == '__main__':
    main()
