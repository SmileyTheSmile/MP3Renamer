import glob
import colorlog
from os.path import splitext

logger = colorlog.getLogger(__name__)


def get_supported_files(directory: str, extensions: list):
    """Returns a list of all the files from a <directory> with the provided <extensions>."""
    files = []
    for ext in extensions:
        string_pattern = f'*.{ext}'
        files.extend(glob.glob1(directory, string_pattern))

    logger.info(f"Loaded all [{', '.join(extensions)}] files from {directory}")

    return files


def splitext_in_list(files: list):
    """Splits the names and extensions of <files> in a list."""
    result = [splitext(file) for file in files]
    logger.debug(result)
    return result
