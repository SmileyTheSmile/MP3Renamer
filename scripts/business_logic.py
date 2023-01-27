from scripts import mp3_renamer as mp3r
from scripts import file_operations as f_op
from scripts import text_formatter as tf
from scripts import func_tester as ft


class BusinessLogic:
    def __init__(self, file_params, default_song_tags, purification_params):
        song_files = f_op.get_supported_files(file_params.directory, file_params.supported_extensions)
        song_files = tf.set_matching_strings(song_files, r"Chainsaw Man OST - \d+ - *", r"\.mp3")

        song_tags = mp3r.get_song_tags(song_files, default_song_tags, purification_params)
        mp3r.apply_tags_to_song_files(song_files, file_params.directory, song_tags)
