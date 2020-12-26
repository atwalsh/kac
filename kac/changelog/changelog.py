import re
from datetime import date, datetime
from typing import Dict

import click
from semver import VersionInfo

from .release import Release, Unreleased
from .util import rreplace


class Changelog:
    default_file_name: str = 'CHANGELOG.md'

    def __init__(self, path: str):
        """
        :param path: The full file system path of the CHANGELOG file.

        Attributes:
            path        The full file system path of the CHANGELOG file.
            full_text   Original CHANGELOG file text.
            unreleased  Unreleased changes.
            releases    List of Release objects for each published release in the CHANGELOG.
        """
        self.path = path

        # Read full Changelog text
        try:
            with click.open_file(self.path) as f:
                self.full_text = f.read()
        except FileNotFoundError:
            click.echo()

        # Parse CHANGELOG header, body, and footer
        m_file = re.fullmatch(r'([\s\S]+)(## \[Unreleased][\s\S]+)(\[Unreleased]:[\s\S]+)', self.full_text)
        self._header_text, self._body_text, self._footer_text = m_file.groups()  # type: str, str, str

        # Parse Unreleased section
        m_unreleased = re.match(r'## \[Unreleased]\n((?:### \w+[\n\s]*(?:-[ \S]*[\s]+)*)*)', self._body_text)
        if m_unreleased is None:
            click.echo('Unable to match CHANGELOG `Unreleased` section.')
            raise click.Abort
        # if m_unreleased.groups()[0].strip() != '':
        self.unreleased = Unreleased(**Unreleased.changes_to_dict(m_unreleased.groups()[0].strip()))

        # Parse releases from the body section
        self.releases = []
        m_releases = re.findall(r'(?:## \[([\S]+)] - ([\d-]+)\s*)((?:### \w+[\n\s]*(?:-[ \S]*[\s]+)*)*)?',
                                self._body_text)
        version_ids = [r[0] for r in m_releases]  # ex: ['Unreleased', '1.0.0', '0.9.0', ...]
        # Parse changes from each release
        for v, d, c in m_releases:  # type: str, str, str # version, date, changes
            c = c.strip()
            self.releases.append(Release(
                **Release.changes_to_dict(c),
                release_date=datetime.strptime(d, '%Y-%m-%d').date(),
                version=VersionInfo.parse(v)
            ))

    def __repr__(self):
        return f'<CHANGELOG v{self.most_recent_version}>'

    @property
    def most_recent_version(self) -> VersionInfo:
        """
        Get the most recent version of the CHANGELOG file.

        :return: VersionInfo instance of most recent semver version.
        """
        return self.most_recent_release.version

    @property
    def most_recent_release(self) -> Release:
        """
        Get the most recent release of the CHANGELOG file

        :return: Release instance for most recent release.
        """
        return self.releases[0]

    def get_next_versions(self, prerelease_token='rc', build_token='build') -> Dict[str, VersionInfo]:
        """
        Get a dictionary of possible new Changelog versions.

        For example, if the current version of the Changelog is v3.6.3, the following dict will be returned:
        {
            'v4.0.0': VersionInfo(major=4, minor=0, patch=0, prerelease=None, build=None),
            'v3.7.0': VersionInfo(major=3, minor=7, patch=0, prerelease=None, build=None),
            'v3.6.4': VersionInfo(major=3, minor=6, patch=4, prerelease=None, build=None),
            'v3.6.3-rc.1': VersionInfo(major=3, minor=6, patch=3, prerelease='rc.1', build=None),
            'v3.6.3+build.1': VersionInfo(major=3, minor=6, patch=3, prerelease=None, build='build.1'),
            'v3.6.3-rc.1+build.1': VersionInfo(major=3, minor=6, patch=3, prerelease='rc.1', build='build.1')
        }

        :param prerelease_token: String to identify prerelease versions, defaults to `rc`.
        :param build_token: String to identify build versions, defaults to `build`.
        :return: Dictionary of possible new Changelog versions.
        """
        versions = (
            self.most_recent_version.bump_patch(),
            self.most_recent_version.bump_minor(),
            self.most_recent_version.bump_major(),
            self.most_recent_version.bump_prerelease(prerelease_token),
            self.most_recent_version.bump_build(build_token),
            self.most_recent_version.bump_prerelease(prerelease_token).bump_build(build_token),
        )
        return {f'v{v}': v for v in versions}

    def bump(self, version: VersionInfo) -> None:
        """
        Bump the CHANGELOG to the specified version.

        :param version: The version which the CHANGELOG file should be bumped to.
        """
        unreleased_url_re_pattern: str = r'\[Unreleased\]:'
        version_diff_pattern: str = '[{new_version}]: {base_url}/{current_version}...{new_version_end}'

        with click.open_file(self.path, mode='w') as f:
            f.write(self._header_text)
            new_body = self._body_text.replace('## [Unreleased]\n', f'## [Unreleased]\n\n## [{version}] -'
                                                                    f' {date.today()}\n')
            f.write(new_body)
            unreleased_url_pattern = re.compile(unreleased_url_re_pattern)
            for line in self._footer_text.splitlines(keepends=False):
                if unreleased_url_pattern.match(line):
                    new_line = rreplace(
                        s=line,
                        old=f'v{self.most_recent_version}',
                        new=f'v{version}',
                        occurrence=1
                    )
                    f.write(f'{new_line}\n')
                    new_diff_url = version_diff_pattern.format(
                        new_version=f'{version}',
                        new_version_end=f'v{version}',
                        current_version=f'{self.most_recent_version}',
                        base_url=re.search("(?P<url>https?://[^\\s]+)", line).group("url").rsplit('/', 1)[0]
                    )
                    f.write(f'{new_diff_url}\n')
                else:
                    f.write(f'{line}\n')
            f.write('\n')
