from eyed3 import load


def change_song_attributes(song_params):
    audiofile = load(song_params["filename"])
    songTag = audiofile.tag

    songTag.title = song_params["title"]
    songTag.artist = song_params["artist"]
    songTag.album = song_params["album"]
    songTag.year = song_params["year"]
    songTag.genre = song_params["genre"]
    songTag.album_artist = song_params["album_artist"]
    songTag.track_num = song_params["track_num"]

    songTag.save()