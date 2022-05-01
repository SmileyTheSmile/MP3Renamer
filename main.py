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
            params["songParams"]["title"] = purifySongName(i[0], params["purificationParams"]).title()
            
            changeSongAttributes(params["songParams"])
    
main()