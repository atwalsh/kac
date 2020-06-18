import re
from typing import Tuple


def parse_version_number(val: str) -> Tuple[int, int, int]:
    """
    Parse a version number. Supports vX.X.X and X.X.X formats.

    :param val: The version number to parse.
    :return: Tuple of ints representing the version.
    """
    _version_re_pattern: str = r'v?(\d+)\.(\d+)\.(\d+)'
    pattern = re.compile(_version_re_pattern)
    match = pattern.match(val)
    if match is None:
        raise ValueError(f'Invalid version number {val}')
    groups = match.groups()
    return int(groups[0]), int(groups[1]), int(groups[2])


def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    """
    Reverse replace.

    :param s: Original string.
    :param old: The character to be replaced.
    :param new: The character that will replace `old`.
    :param occurrence: The number of occurrences of `old` that should be replaced with `new`.
    """
    return new.join(s.rsplit(old, occurrence))
