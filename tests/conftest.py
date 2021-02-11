from pathlib import Path

import pytest

from kac.changelog import Changelog


@pytest.fixture
def test_changelog_path():
    return f'{Path(__file__).parent.resolve()}/files/test_changelog_file.md'


@pytest.fixture(scope='function')
def test_changelog(test_changelog_path):
    return Changelog(test_changelog_path)
