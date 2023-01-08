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


def set_matching_strings(strings_list: list, pattern: str):
    result = [compile(pattern).sub('', string) for string in strings_list]
    logger.debug(result)
    return result

    # return list(filter(compile(pattern).sub('', string), strings_list))
