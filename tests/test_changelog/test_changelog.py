from collections import OrderedDict
from datetime import date
from pathlib import Path

import pytest
from click.exceptions import Abort
from semver import VersionInfo

from kac.changelog import Changelog


class TestChangelog:
    def test_init(self):
        path = f'{Path(__file__).parent.resolve()}/test_changelog_file.md'
        with open(path, 'r') as f:
            expected_full_text = f.read()

        c = Changelog(path)
        assert c.path == path

        assert c.unreleased.has_changes
        assert c.unreleased.added == ['Something added']
        assert c.unreleased.changed == ['`template` command to `new`']
        assert not any([c.unreleased.deprecated, c.unreleased.deprecated, c.unreleased.removed, c.unreleased.security])

        assert len(c.releases) == 9
        assert c.releases[0].version == VersionInfo(0, 3, 0)
        assert c.releases[0].release_date == date(2020, 4, 5)
        assert c.releases[-1].version == VersionInfo(0, 1, 0)

        assert c.full_text == expected_full_text

    def test_init_bad_path(self, tmp_path):
        with pytest.raises(Abort) as e_info:
            Changelog(str(tmp_path) + '/CHANGELOG.md')

    def test_most_recent_version(self):
        path = f'{Path(__file__).parent.resolve()}/test_changelog_file.md'
        c = Changelog(path)
        assert c.most_recent_release

    def test_get_next_versions(self):
        path = f'{Path(__file__).parent.resolve()}/test_changelog_file.md'
        c = Changelog(path)
        assert c.get_next_versions() == OrderedDict({
            'v0.3.1': VersionInfo(0, 3, 1),
            'v0.4.0': VersionInfo(0, 4),
            'v1.0.0': VersionInfo(1),
            'v0.3.0-rc.1': VersionInfo(0, 3, prerelease='rc.1'),
            'v0.3.0+build.1': VersionInfo(0, 3, build='build.1'),
            'v0.3.0-rc.1+build.1': VersionInfo(0, 3, prerelease='rc.1', build='build.1'),
        })
