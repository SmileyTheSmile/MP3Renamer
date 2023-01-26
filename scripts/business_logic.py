from scripts.mp3_renamer import MP3Renamer
from scripts import file_operations as f_op
from scripts.text_formatter import set_matching_strings, get_matching_strings
import logging.config


class BusinessLogic:
    def __init__(self):
        pass
        '''
        logging.config.fileConfig('resources/logging.ini', disable_existing_loggers=False)

        file_params, default_song_tags, purification_params = ui.get_params_from_UI()

        song_files = f_op.get_supported_files(file_params.song_dir_name, file_params.supported_extensions)
        song_files = get_matching_strings(song_files, r"Chainsaw Man OST - \d+ - ([a-zA-Z]+( [a-zA-Z]+)+)\.mp3")
        song_files = set_matching_strings(song_files, r"Chainsaw Man OST - \d+ - *")

        if file_params.rename_files:
            f_op.rename_file(file, song_tags.title + file_extension)

        song_files_split = f_op.splitext_in_list(song_files)

        mp3_renamer = MP3Renamer()
        song_tags = mp3_renamer.get_song_tags(song_files_split, default_song_tags, purification_params)
        mp3_renamer.apply_tags_to_song_files(song_files, file_params.song_dir_name, song_tags)
        '''
