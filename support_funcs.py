from enum import Enum
from os.path import isfile, splitext, join
from os import listdir
from pathlib import Path


def purifySongName(songName, purificationParams):
    if purificationParams["purificationMode"] == PurificationMode.splitBySymbol:
        songName = songName.split(purificationParams["splitSymbol"])[purificationParams["splitIndex"]]
        
    elif purificationParams["purificationMode"] == PurificationMode.removeClutter:
        songName = songName.split()
        for i in range(len(songName)):
            if i in purificationParams["clutterIndexes"]:
                songName[i] = ''
        ' '.join(songName)
    elif purificationParams["purificationMode"] == PurificationMode.sliceOffEnds:
        songName = songName.split()[purificationParams["leftEnd"] : purificationParams["rightEnd"]]
        songName = ' '.join(songName)

    print(songName)
    return songName


def getFilesFromDir(songDirName):
    songDir = Path(songDirName).resolve()
    songFiles = [splitext(f) for f in listdir(songDir) if isfile(join(songDir, f))]

    return songFiles


class PurificationMode(Enum):
    splitBySymbol = 1
    removeClutter = 2
    sliceOffEnds  = 3
