from mutagen import File
from mutagen.easyid3 import EasyID3
from scripts.utilities.data_classes import SongTags


def get_song_tags(files, default_tags, purification_params):
    """Returns a dictionary, where the keys are song file names and the items
    are <default_tags> with song titles generated from <files> using <purification_params>"""
    tags = {}
    for name, extension in files:
        default_tags.title = purify_song_title(name, purification_params)
        tags[f"{name}{extension}"] = default_tags
    return tags

def set_songs_tags(songs: list, tags: SongTags):
    """Set MP3 <tags> of <songs>."""
    for song in songs:
        song.update_files(vars(tags))

def generate_songs(files: list) -> list:
    """Generates Mutagen song objects for <files>."""
    for file in files:
        file.song = File(file.path, ID3=EasyID3)
    return files
