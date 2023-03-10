from dataclasses import dataclass, field
from mutagen import FileType


@dataclass
class Settings:
    initial_directory = "E:/My Stuff/My Programs/MP3Renamer/songs"
    allowed_extensions = [".mp3", ".mp4"]


@dataclass
class FileInfo:
    directory: str = ""
    name: str = ""
    extension: str = ""
    song: FileType = None

    def __int__(self, directory, name, extension):
        self.directory = directory
        self.name = name
        self.extension = extension
    def path(self):
        return f"{self.path}{self.name}{self.extension}"
    def filename(self):
        return f"{self.name}{self.extension}"


@dataclass
class SongTags:
    title: str = ""
    artist: str = ""
    album: str = ""
    date: str = ""
    genre: str = ""
    albumartist: str = ""
    tracknumber: str = ""
