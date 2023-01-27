from dataclasses import dataclass, field
from enum import Enum


class PurificationMode(Enum):
    """Set the way in which the clutter is removed from the song titles."""
    none = 0
    splitBySymbol = 1
    removeSymbolsAtIndexes = 2
    sliceOffEnds = 3


@dataclass
class SongTags:
    artist: str = ""
    album: str = ""
    date: str = ""
    genre: str = ""
    albumartist: str = ""
    tracknumber: str = ""


@dataclass
class FileParams:
    directory: str = "E:/My Stuff/My Programs/MP3Renamer/songs"
    supported_extensions: list = field(default_factory=lambda: ["mp3"])
    rename_files: bool = False


@dataclass
class PurificationParams:
    mode: PurificationMode = field(default_factory=lambda: PurificationMode.splitBySymbol)
    split_symbol: str = " - "
    split_index: int = 1
    clutter_indexes: list = field(default_factory=lambda: [])
    left_end: int = None
    right_end: int = None
