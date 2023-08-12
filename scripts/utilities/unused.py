from re import compile, Pattern
from os.path import splitext
from enum import Enum
import time


def test_wrap(function, *args, **kwargs):
    start = time.perf_counter()
    result = function(*args, **kwargs)
    end = time.perf_counter()

    print(f"{end - start}")

    return result

def test(function, *args, **kwargs):
    start = time.perf_counter()
    function(*args, **kwargs)
    end = time.perf_counter()

    print(f"{end - start}")


class PurificationMode(Enum):
    """Set the way in which the clutter is removed from the song titles."""
    none = 0
    splitBySymbol = 1
    removeSymbolsAtIndexes = 2
    sliceOffEnds = 3


purification_modes = {
    PurificationMode.splitBySymbol:
        lambda title, params:
        split_by_symbol(title, params.split_symbol, params.split_index),
    PurificationMode.sliceOffEnds:
        lambda title, params:
        split_by_symbol(title, params.left_end, params.right_end)
}


def splitext_in_list(files: list):
    """Splits the names and extensions of <files> in a list."""
    result = [splitext(file) for file in files]
    return result

def remove_pattern(string: str, pattern: Pattern):
    """Removes the leftmost instance of a regex <pattern> from <string>."""
    return pattern.sub('', string)

def split_by_symbol(string: str, symbol: str, result_index: int) -> str:
    """
    Splits the string by the <symbol> and returns the string
    at the <result_index>.
    Example: split_by_symbol("1 - songname", 1) -> "songname"
    """
    return string.split(symbol)[result_index]


def remove_symbols_at_indexes(string: str, indexes: list) -> str:
    """
    Splits the string with the <symbol> parameter and returns the string
    at the <result_index>.
    Example: split_by_symbol("son-gna-me", [3, 7]) -> "songname"
    """
    for i in indexes:
        string[i] = ''
    return string


def slice_off_ends(string: str, left: int, right: int) -> str:
    """
    Cuts off the beginning and the ending of a string
    Example: slice_off_ends("author - [songname]", [3, 7]) -> "songname"
    """
    return string[left: right]


def set_matching_strings_old(strings_list: list, pattern: str):
    result = [compile(pattern).sub('', string) for string in strings_list]
    return result

    # return list(filter(compile(pattern).sub('', string), strings_list))

def splitext_in_list(files: list):
    """Splits the names and extensions of <files> in a list."""
    result = [splitext(file) for file in files]
    return result
