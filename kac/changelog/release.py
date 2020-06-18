from datetime import date
from typing import Tuple


class Release:
    """
    Represents a release in a Changelog file.
    """
    def __init__(self, version: Tuple[int, int, int], release_date: date, release_text: str):
        self.version = version
        self.release_date = release_date
        self.release_text = release_text
