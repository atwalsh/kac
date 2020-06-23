import pytest

from kac.changelog.util import parse_version_number


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
            parse_version_number(vn)

    assert parse_version_number('v1.0.0') == (1, 0, 0)
    assert parse_version_number('1.0.0') == (1, 0, 0)
    assert parse_version_number('0.0.1') == (0, 0, 1)
