import tkinter


def getParamsFromUI():
    songDirName = "E:\My Stuff\My Programs\MP3Renamer\songs"
    
    artist = "Joe Hisaishi"
    album = "Howl's Moving Castle"
    year = "2004"
    genre = "Orchestral"
    album_artist = None
    track_num = None
    
    params = {
        "songDirName": songDirName,
        "songParams": {
            "artist": artist,
            "album": album,
            "year": year,
            "genre": genre,
            "album_artist": album_artist,
            "track_num": track_num
            }
        }
    
    return params