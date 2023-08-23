from re import compile, Pattern
import colorlog

# https://regex-generator.olafneumann.org/?sampleText=Arg..mp3&flags=i&selection=3%7CCharacter,0%7CAlphanumeric%20characters
# https://docs.python.org/3/library/re.html

logger = colorlog.getLogger(__name__)


def get_matching_strings(strings_list: list, pattern: str):
    """Returns all the strings from <strings_list> that match the regex <pattern>."""
    pattern = compile(pattern)
    result = list(filter(pattern.match, strings_list))
    logger.debug(result)
    return result

def apply_patterns_to_list(strings_list: list, patterns: list):
    """Applies a list of regex <patterns> to a <strings_list>"""
    patterns = compile_patterns(patterns)
    for i, string in enumerate(strings_list):
        strings_list[i] = remove_patterns(string, patterns)
    logger.debug(strings_list)
    return strings_list

def remove_patterns(string: str, patterns: list):
    """Sequentially removes the leftmost instance of all regex <patterns> from <string>."""
    for pattern in patterns:
        string = pattern.sub('', string)
    return string

def compile_patterns(patterns: list):
    """Returns a list of compiled regex <patterns>."""
    return [compile(pattern) for pattern in patterns]