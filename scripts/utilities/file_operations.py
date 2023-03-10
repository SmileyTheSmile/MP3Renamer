import glob
from os import listdir
from os.path import splitext

from scripts.utilities import data_classes as data

def load_supported_files(directory: str, extensions: list) -> list:
    """
    Returns a list of filenames with specified <extensions> from a <directory>.
    """
    string_pattern = f"*[{'|'.join(extensions)}]"
    files = glob.glob1(directory, string_pattern)
    return files

def load_files(directory: str) -> list:
    """Returns a list of filenames from a <directory>."""
    return listdir(directory)

def convert_to_file_info(directory: str, files: list) -> list:
    """Returns a list of FileInfo objects of the <files> in a <directory>."""
    return [data.FileInfo(directory, *splitext(file)) for file in files]
