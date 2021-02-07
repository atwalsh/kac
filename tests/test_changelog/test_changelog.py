from collections import OrderedDict
from datetime import date
from pathlib import Path

import pytest
from click.exceptions import Abort
from freezegun import freeze_time
from semver import VersionInfo

from kac.changelog import Changelog, Release


class TestChangelog:
    @pytest.fixture
    def test_changelog_path(self):
        return f'{Path(__file__).parent.resolve()}/test_changelog_file.md'

    @pytest.fixture(scope='function')
    def test_changelog(self, test_changelog_path):
        return Changelog(test_changelog_path)

    def test_init(self, test_changelog, test_changelog_path):
        with open(test_changelog_path, 'r') as f:
            expected_full_text = f.read()

        c = Changelog(test_changelog_path)
        assert c.path == test_changelog_path

        assert c.unreleased.has_changes
        assert c.unreleased.added == ['Something added']
        assert c.unreleased.changed == ['`template` command to `new`']
        assert not any([c.unreleased.deprecated, c.unreleased.deprecated, c.unreleased.removed, c.unreleased.security])

        assert len(c.releases) == 9
        assert c.releases[0].version == VersionInfo(0, 3, 0)
        assert c.releases[0].release_date == date(2020, 4, 5)
        assert c.releases[-1].version == VersionInfo(0, 1, 0)

        assert c.full_text == expected_full_text

    def test_init_no_unreleased(self, test_changelog_path, tmp_path):
        """Check a click `Abort` is raised if the CHANGELOG has no `Unreleased` section."""
        path = tmp_path
        f_path = path / 'CHANGELOG.md'
        with open(test_changelog_path) as f:
            lines = f.readlines()

        # Remove released section by line numbers 😕
        f_path.write_text(''.join([l for idx, l in enumerate(lines) if idx not in range(5, 12)]))

        with pytest.raises(Abort):
            Changelog(str(f_path))

    def test_repr(self, test_changelog):
        assert test_changelog.__repr__() == f'<CHANGELOG v0.3.0>'

    def test_init_bad_path(self, tmp_path):
        with pytest.raises(Abort):
            Changelog(str(tmp_path) + '/CHANGELOG.md')

    def test_latest_version(self, test_changelog):
        assert test_changelog.latest_version == VersionInfo(0, 3, 0)

    def test_latest_release(self, test_changelog):
        r = Release(
            VersionInfo(0, 3),
            date(2020, 4, 5),
            added=[
                '`template` command',
                'Initial basic tests with SemaphoreCI integration',
                'Automatic releases to PyPI on git tags'
            ],
            changed=['Use poetry instead of pipenv'],
        )
        assert test_changelog.latest_release == r

    def test_get_next_versions(self, test_changelog):
        assert test_changelog.get_next_versions() == OrderedDict({
            'v0.3.1': VersionInfo(0, 3, 1),
            'v0.4.0': VersionInfo(0, 4),
            'v1.0.0': VersionInfo(1),
            'v0.3.0-rc.1': VersionInfo(0, 3, prerelease='rc.1'),
            'v0.3.0+build.1': VersionInfo(0, 3, build='build.1'),
            'v0.3.0-rc.1+build.1': VersionInfo(0, 3, prerelease='rc.1', build='build.1'),
        })

        assert test_changelog.get_next_versions(prerelease_token='pr', build_token='bo') == OrderedDict({
            'v0.3.1': VersionInfo(0, 3, 1),
            'v0.4.0': VersionInfo(0, 4),
            'v1.0.0': VersionInfo(1),
            'v0.3.0-pr.1': VersionInfo(0, 3, prerelease='pr.1'),
            'v0.3.0+bo.1': VersionInfo(0, 3, build='bo.1'),
            'v0.3.0-pr.1+bo.1': VersionInfo(0, 3, prerelease='pr.1', build='bo.1'),
        })

    @freeze_time('2021-01-16')
    def test_bump(self, test_changelog_path, tmp_path):
        c_path = tmp_path / 'CHANGELOG.md'
        with open(test_changelog_path, 'r') as f:
            c_path.write_text(f.read())
        changelog = Changelog(str(c_path))
        changelog_unr = changelog.unreleased  # Pre-bump unreleased changed

        # Bump
        assert changelog.latest_version == VersionInfo(0, 3)
        changelog.bump(VersionInfo(0, 4))
        assert changelog.latest_version == VersionInfo(0, 4)

        # Check that the changelog's unreleased and releases were updated
        assert not changelog.unreleased.has_changes

        assert changelog.latest_release == Release(VersionInfo(0, 4), date(2021, 1, 16))
        assert changelog.latest_release.changed == changelog_unr.changed
        assert changelog.latest_release.added == changelog_unr.added
        assert not any([
            changelog.latest_release.deprecated,
            changelog.latest_release.fixed,
            changelog.latest_release.removed,
            changelog.latest_release.security,
        ])

        # Verify bumped CHANGELOG text
        bumped_path = f'{Path(__file__).parent.resolve()}/test_changelog_file_bumped.md'
        with open(bumped_path, 'r') as expected_f, open(c_path, 'r') as actual_f:
            assert expected_f.read() == actual_f.read()
