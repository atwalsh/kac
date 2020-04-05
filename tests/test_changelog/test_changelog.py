import pytest

from kac.changelog import Changelog


def test_parse_version_number():
    invalid_version_numbers = (
        '',
        '1.0',
        'v.1.0.0',
        'v1.0.'
        'v1.0',
        'v1.0.a'
    )
    for vn in invalid_version_numbers:
        with pytest.raises(ValueError):
            Changelog.parse_version_number(vn)

    assert Changelog.parse_version_number('v1.0.0') == (1, 0, 0)
    assert Changelog.parse_version_number('1.0.0') == (1, 0, 0)
    assert Changelog.parse_version_number('0.0.1') == (0, 0, 1)
