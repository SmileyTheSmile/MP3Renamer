from re import compile
import colorlog

logger = colorlog.getLogger(__name__)


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


def get_matching_strings(strings_list: list, regex_pattern: str):
    """Returns all the strings from <strings_list> that match the <pattern>."""
    result = list(filter(compile(regex_pattern).match, strings_list))
    logger.debug(result)
    return result


def set_matching_strings_old(strings_list: list, pattern: str):
    result = [compile(pattern).sub('', string) for string in strings_list]
    logger.debug(result)
    return result

    # return list(filter(compile(pattern).sub('', string), strings_list))

def set_matching_strings(strings_list: list, pattern_left: str, pattern_right: str):
    pattern_left = compile(pattern_left)
    pattern_right = compile(pattern_right)
    for i, string in enumerate(strings_list):
        string = pattern_left.sub('', string)
        strings_list[i] = pattern_right.sub('', string)
    logger.debug(strings_list)
    return strings_list
