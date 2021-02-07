from collections import OrderedDict
from datetime import date

import click
import pytest
from semver import VersionInfo

from kac.changelog.release import ReleaseBase, Release, Unreleased


class TestReleaseBase:
    def test_init_empty(self):
        rb = ReleaseBase()
        assert rb.changes == OrderedDict(
            [('added', []), ('changed', []), ('deprecated', []), ('fixed', []), ('removed', []), ('security', [])])

    def test_init(self):
        rb = ReleaseBase(['Added something'], removed=['Removed A', 'Removed B'])
        assert rb.changes['added'] == ['Added something']
        assert rb.changes
        assert not any([
            rb.changes['changed'],
            rb.changes['deprecated'],
            rb.changes['fixed'],
            rb.changes['security'],
        ])

    def test_changes_to_dict(self):
        changes = '### Added\n- Add A\n\n### Changed\n- Change B\n'
        cd = ReleaseBase.changes_to_dict(changes)
        assert dict(cd) == {
            'added': ['Add A'],
            'changed': ['Change B'],
            'deprecated': [],
            'fixed': [],
            'removed': [],
            'security': []
        }

    def test_changes_to_dict_invalid_item(self):
        changes = '### BadChange\n- Add A\n\n### Changed\n- Change B\n'
        with pytest.raises(click.Abort):
            ReleaseBase.changes_to_dict(changes)

    def test_changes_text(self):
        rb = ReleaseBase(['Added something'], ['Changed A'])
        assert rb.changes_text == '### Added\n- Added something\n\n### Changed\n- Changed A\n\n'


class TestRelease:
    def test_init(self):
        r = Release(VersionInfo(0, 3), date(2021, 2, 11), ['Added something'], removed=['Removed A'])
        assert r.version == VersionInfo(0, 3, 0)
        assert r.release_date == date(2021, 2, 11)
        assert r.__repr__() == f'<Release v0.3.0 - 2021-02-11>'

        # Equality only checks date and release number
        assert r == Release(VersionInfo(0, 3), date(2021, 2, 11), changed=['Changed A'])


class TestUnreleased:
    def test_init(self):
        u = Unreleased()
        assert u.__repr__() == '<Unreleased>'

    def test_has_changes(self):
        u0 = Unreleased()
        assert not u0.has_changes

        u1 = Unreleased(['Add A'], ['Change B'])
        assert u1.has_changes
