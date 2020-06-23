import pendulum

from .section import Section
from ..release import Release
from ..util import parse_version_number


class Body(Section):
    """
    Represents the body section of the Changelog, consisting of all release history for the Changelog.
    """
    _regex_pattern = r'(#{2} \[([\S]*)\](?: - ([\d-]*)[\n\s])*)((#{3} \w+[\n\s]*(?:-[ \S]*[\n\s]+)*)+)*'

    def __init__(self, full_changelog_text):
        super().__init__(full_changelog_text)
        try:
            assert self.matches[0][1] == 'Unreleased'
        except (AssertionError, KeyError):
            raise RuntimeError('CHANGELOG is missing an Unreleased section.')
        # Get the list of releases, excluding the Unreleased section
        self.releases = [
            Release(
                version=parse_version_number(r[1]),
                release_date=pendulum.parse(r[2]).date(),
                release_text=r[3]
            )
            for r in self.matches[1:]
        ]
