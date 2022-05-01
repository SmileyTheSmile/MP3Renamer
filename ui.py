import tkinter
from support_funcs import PurificationMode


def getParamsFromUI():
    songDirName = "E:\My Stuff\My Programs\MP3Renamer\songs"
    
    artist = "Joe Hisaishi"
    album = "Howl's Moving Castle"
    year = "2004"
    genre = "Orchestral"
    album_artist = None
    album_artist = None
    track_num = None
    
    purificationMode = PurificationMode.sliceOffEnds
    splitSymbol = None
    splitIndex = None
    clutterIndexes = None
    leftEnd = 1
    rightEnd = None
    
    params = {
        "songDirName": songDirName,
        "songParams": {
            "artist": artist,
            "album": album,
            "year": year,
            "genre": genre,
            "album_artist": album_artist,
            "track_num": track_num
        },
        "purificationParams": {
            "purificationMode": purificationMode,
            "splitSymbol": splitSymbol,
            "splitIndex": splitIndex,
            "clutterIndexes": clutterIndexes,
            "leftEnd": leftEnd,
            "rightEnd": rightEnd
        }
    }
    
    return params