def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    """
    Reverse replace.

    :param s: Original string.
    :param old: The character to be replaced.
    :param new: The character that will replace `old`.
    :param occurrence: The number of occurrences of `old` that should be replaced with `new`.
    """
    return new.join(s.rsplit(old, occurrence))
