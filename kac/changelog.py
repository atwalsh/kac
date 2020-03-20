import os
import re
from datetime import date
from shutil import move
from tempfile import NamedTemporaryFile
from typing import Tuple, Dict, Union

import click
import pyperclip

rreplace = lambda s, old, new, occurrence: new.join(s.rsplit(old, occurrence))  # Reverse replace


class Changelog:
    # Regex patterns
    _version_title_re_pattern: str = '\#\#\s\[(\d+)\.(\d+)\.(\d+)\].*'
    _version_re_pattern: str = 'v?(\d+)\.(\d+)\.(\d+)'
    _unreleased_url_re_pattern: str = '\[Unreleased\]:'
    _unreleased_tag_re_pattern: str = f'\#\#\s\[Unreleased\].*'
    # Changelog version and diff URL base strings
    _version_pattern: str = '{0}.{1}.{2}'
    _version_diff_pattern: str = '[{new_version}]: {base_url}/{current_version}...{new_version_end}'
    # Default Changelog file name
    default_file_name: str = 'changelog.md'
    LATEST = 'LATEST'

    def __init__(self, changelog_file_name: str = default_file_name):
        self.changelog_file_path = self._get_changelog_file_path(changelog_file_name)
        self.major, self.minor, self.patch = self._get_most_recent_version()

    def __repr__(self):
        return f'<Changelog v{self.major}.{self.minor}.{self.patch}>'

    @classmethod
    def parse_version_number(cls, val: str) -> Tuple[int, int, int]:
        """
        Parse a version number. Supports vX.X.X and X.X.X formats.
        :param val: The version number to parse.
        :return: Tuple of ints representing the version.
        """
        pattern = re.compile(cls._version_re_pattern)
        match = pattern.match(val)
        if match is None:
            raise ValueError(f'Invalid version number {val}')
        groups = match.groups()
        return (int(groups[0]), int(groups[1]), int(groups[2]))

    @staticmethod
    def _get_changelog_file_path(f_name: str) -> str:
        """
        Search for a Changelog file.

        :param f_name: The file name of the Changelog to search for.
        :rtype: str
        :return: Full path of the Changelog file.
        """
        files = [filename for filename in os.listdir(os.getcwd()) if filename.lower() == f_name.lower()]
        num_files = len(files)
        if num_files > 1:
            raise Exception(f'Found multiple Changelog files. {num_files} files found.')
        elif num_files == 0:
            raise Exception('No Changelog file found.')
        return os.path.abspath(files[0])

    def _get_most_recent_version(self) -> Tuple[int, int, int]:
        """
        Get the most recent version from the Changelog file.

        :rtype: (int, int, int)
        :return: Three ints, representing major, minor, and patch version numbers.
        """
        pattern = re.compile(self._version_title_re_pattern)
        with open(self.changelog_file_path) as f:
            for line in f:
                match = pattern.match(line)
                if match:
                    g = match.groups()
                    try:
                        return int(g[0]), int(g[1]), int(g[2])
                    except ValueError:
                        raise Exception('Invalid version number, could not convert to int.')

    def bump(self, new_version: Tuple[int, int, int]) -> None:
        """
        Bump the Changelog version to `new_version` number. This method writes each line of the current Changelog file
        to a temp file, writing new lines when needed, then moves the temp file to the same location as the current
        Changelog file.

        :param new_version: Tupble of new version major, minor, and patch numbers.
        :return: None
        """
        unreleased_tag_pattern = re.compile(self._unreleased_tag_re_pattern)
        unreleased_url_pattern = re.compile(self._unreleased_url_re_pattern)

        # Read current file, write to temp file
        with open(self.changelog_file_path) as f, NamedTemporaryFile(dir=".", delete=False) as out:
            for line in f:
                if unreleased_url_pattern.match(line):  # If this line matches the Unreleased diff URL pattern
                    new_line = rreplace(
                        s=line,
                        old=self.format_version((self.major, self.minor, self.patch)),
                        new=self.format_version(new_version),
                        occurrence=1
                    )
                    out.write(new_line.encode())
                    new_diff_url = self._version_diff_pattern.format(
                        new_version=self.format_version(new_version, include_v=False),
                        new_version_end=self.format_version(new_version),
                        current_version=self.format_version((self.major, self.minor, self.patch)),
                        base_url=re.search("(?P<url>https?://[^\\s]+)", line).group("url").rsplit('/', 1)[0]
                    )
                    out.write(f'{new_diff_url}\n'.encode())
                elif unreleased_tag_pattern.match(line):  # If this line matches the Unreleased tag pattern
                    out.write(f'{line}\n'.encode())
                    out.write(
                        f'## [{self.format_version(new_version, include_v=False)}] - {str(date.today())}\n'.encode())
                else:  # Write the line as-is
                    out.write(line.encode())
        move(out.name, self.changelog_file_path)  # Move the temp file to the current Changelog file location
        out.close()  # Close temp file

    def copy_release_text(self, v: Union[LATEST, Tuple[int, int, int]] = LATEST) -> None:
        """
        Copy the requested version's release text to the clipboard.

        :param v: The version to copy release text for.
        :return: Nothing.
        """
        version: Tuple[int, int, int] = self._get_most_recent_version() if v == self.LATEST else v
        save_lines = False  # Whether or not we should be saving lines
        text = ''
        pattern = re.compile(self._version_title_re_pattern)
        with open(self.changelog_file_path) as f:
            for line in f:  # Run through each line of the CHANGELOG
                if save_lines:
                    # Stop saving release text if the line matches the release title regex pattern
                    if pattern.match(line):
                        save_lines = False
                    # Add the line to the release text we need to copy
                    else:
                        text += line
                else:
                    match = pattern.match(line)
                    if match and self.parse_version_number(
                            f'{match.groups()[0]}.{match.groups()[1]}.{match.groups()[2]}') == version:
                        save_lines = True
        if not text:
            raise LookupError(f'Could not find version number {self.format_version(v, include_v=True)}')
        pyperclip.copy(text.rstrip('\n '))
        click.echo(f'{self.format_version(version, include_v=True)} release text copied to clipboard!')

    def format_version(self, v: Tuple[int, int, int], include_v: bool = True) -> str:
        """
        Format a group of major, minor, and patch version numbers to the `MAJOR.MINOR.PATCH` format. Optionally prepend
        the `v` character.

        :param v: Tuple containing the major, minor, and patch version numbers.
        :param include_v: Whether or not to include the starting `v` character.
        :rtype: str
        :return: Formatting version string.
        """
        v = self._version_pattern.format(*v)
        return 'v' + v if include_v else v

    @property
    def available_new_versions(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Dictionary of possible new Changelog versions in the following format:
            {VERSION_NUMBER: str, VERSION_TUPLE: Tuple[int, int, int]}

        For example, if the current version of the Changelog is v3.6.3, the following dict will be returned:
        {
            'v3.6.4': (3, 6, 4),
            'v3.7.0': (3, 7, 0),
            'v4.0.0': (4, 0, 0)
        }

        :rtype: dict
        :return: Dictionary of possible new Changelog versions.
        """
        return {self._version_pattern.format(*v): v for v in (self.new_patch, self.new_minor, self.new_major)}

    @property
    def new_major(self) -> Tuple[int, int, int]:
        """Bump the Changelog major version."""
        return self.major + 1, 0, 0

    @property
    def new_minor(self) -> Tuple[int, int, int]:
        """Bump the Changelog minor version."""
        return self.major, self.minor + 1, 0

    @property
    def new_patch(self) -> Tuple[int, int, int]:
        """Bump the Changelog patch version."""
        return self.major, self.minor, self.patch + 1
