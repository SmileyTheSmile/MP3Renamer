from eyed3 import load


def changeSongAttributes(songParams):
    audiofile = load(songParams["filename"])
    songTag = audiofile.tag

    songTag.title = songParams["title"]
    songTag.artist = songParams["artist"]
    songTag.album = songParams["album"]
    songTag.year = songParams["year"]
    songTag.genre = songParams["genre"]
    songTag.album_artist = songParams["album_artist"]
    songTag.track_num = songParams["track_num"]

    songTag.save()