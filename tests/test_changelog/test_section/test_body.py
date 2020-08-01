from datetime import date
from pathlib import Path

import pytest

from kac.changelog.release import Release
from kac.changelog.section import Body


class TestBody:
    def test_regex_pattern(self):
        assert Body._regex_pattern == r'(## \[([\S]+)\](?: - ([\d-]+))?\s*)((?:#{3} \w+[\n\s]*(?:-[ \S]*[\n\s]+)*)*)'

    def test_init_no_unreleased_section(self):
        with pytest.raises(RuntimeError) as e:
            with open(f'{Path(__file__).parent.resolve()}/_templates/test_init_no_unreleased_section.md', 'r') as exp_f:
                Body(exp_f.read())
        assert str(e.value) == 'CHANGELOG is missing an Unreleased section.'

    def test_init_releases(self):
        with open(f'{Path(__file__).parent.resolve()}/_templates/test_init_releases.md', 'r') as exp_f:
            body = Body(exp_f.read())
        assert body.releases == [
            Release((0, 2, 0), date(2020, 2, 10), '### Changed\n- Testing\n\n'),
            Release((0, 0, 1), date(2020, 7, 1), '### Added\n- Testing\n\n')
        ]
