from kac.changelog.section import Header


class TestHeader:
    def test_regex_pattern(self):
        assert Header._regex_pattern == r'([\s\S]+)## \[Unreleased\]'
