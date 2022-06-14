from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def change_song_attributes(song_params):
    song = MP3(song_params["filename"], ID3=EasyID3)

    try: song["title"] = song_params["title"]
    except: song["title"] = ""
        
    try: song["artist"] = song_params["artist"]
    except: song["title"] = ""
        
    try: song["album"] = song_params["album"]
    except: song["title"] = ""
        
    try: song["date"] = song_params["date"]
    except: song["title"] = ""
    
    try: song["genre"] = song_params["genre"]
    except: song["title"] = ""
    
    try: song["albumartist"] = song_params["albumartist"]
    except: song["albumartist"] = ""
    
    try: song["tracknumber"] = song_params["tracknumber"]
    except: song["title"] = ""
    
    song.save()
