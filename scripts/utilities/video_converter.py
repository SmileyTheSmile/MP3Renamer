from converter import Converter
conv = Converter()

info = conv.probe('Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4')

convert = conv.convert(
    '/home/dannyboy/Documents/Projects/MP3Renamer/Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4',
    '/home/dannyboy/Documents/Projects/MP3Renamer/test1.mp3', {
    'format': 'mp3',
    'audio': {
        'codec': 'mp3',
        'samplerate': 320,
        },
    })

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')