import re
from abc import ABCMeta, abstractmethod
from typing import Tuple, List


class Section(metaclass=ABCMeta):
    """
    Represents a part of the Changelog file.
    """

    def __init__(self, full_changelog_text):
        """
        Create a new Section.

        :param full_changelog_text: A string containing the full text of the CHANGELOG file.
        """
        self.text, self.matches = self._parse_section_text(full_changelog_text)

    @property
    @abstractmethod
    def _regex_pattern(self) -> str:
        """
        Regex pattern to match against for this section.

        :raises: NotImplementedError if the attribute is not implemented.
        :return: Regex pattern to match for this section.
        """
        raise NotImplementedError

    def _parse_section_text(self, text) -> Tuple[str, List[Tuple[str]]]:
        """
        Parse the Section text from the full Changelog text.

        :param text: The full text of the Changelog.
        :return: A two-element tuple, where the first element is a full-match, and the second element is a list of
            tuples for each group in the match.
        """
        matches = re.compile(self._regex_pattern).findall(text)
        r_val = ''.join([group[0] + '\n' for group in matches]).rstrip('\n')
        if not r_val:
            raise ValueError
        return r_val, matches
