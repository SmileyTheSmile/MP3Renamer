from enum import Enum
from os.path import isfile, splitext, join
from os import listdir
from pathlib import Path


def pureSongName(songName):
    #if purificationMode != None:
    #    songName = songName.split(splitValue)[splitIndex]

    return songName


def getFilesFromDir(songDirName):
    songDir = Path(songDirName).resolve()
    songFiles = [splitext(f) for f in listdir(songDir) if isfile(join(songDir, f))]

    return songFiles


def capitalizeAllWords(songName):
    songName = songName.split()

    for i in songName:
        i.capitalize()

    return ' '.join(songName)


class BugStatus(Enum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1
