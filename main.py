from music import  *
from ui import *
from support_funcs import *
from os import chdir, getcwd


def main():
    params = getParamsFromUI()
    
    songFiles = getFilesFromDir(params["songDirName"])
    
    chdir(params["songDirName"])
    
    for i in songFiles:
        if i[1] == ".mp3":
            params["songParams"]["filename"] = ''.join(i)
            params["songParams"]["title"] = capitalizeAllWords(pureSongName(i[0]))
            
            changeSongAttributes(params["songParams"])
    
main()