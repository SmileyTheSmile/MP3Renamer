import glob
import colorlog
from os.path import splitext
from os import listdir

logger = colorlog.getLogger(__name__)


def get_supported_files(directory: str, extensions: list):
    """
    Returns a dictionary of all the files from a <directory>,
    where the keys are the provided <extensions> and the items are lists of file names.
    """
    string_pattern = f"*[{'|'.join(extensions)}]"
    result = glob.glob1(directory, string_pattern)

    logger.info(f"Loaded all [{', '.join(extensions)}] files from {directory}")
    logger.debug(result)

    return result

def get_supported_files_alt(directory: str, extensions: list):
    """
    Returns a dictionary of all the files from a <directory>,
    where the keys are the provided <extensions> and the items are lists of file names.
    """
    result = {extension: [] for extension in extensions}
    files = listdir(directory)

    for file in files:
        name, extension = splitext(file)
        if extension in extensions:
            result[extension].append(name)

    logger.info(f"Loaded all [{', '.join(extensions)}] files from {directory}")
    logger.debug(result)

    return result

def splitext_in_list(files: list):
    """Splits the names and extensions of <files> in a list."""
    result = [splitext(file) for file in files]
    logger.debug(result)
    return result
