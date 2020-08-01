from kac.changelog.section import Footer


class TestFooter:
    def test_regex_pattern(self):
        assert Footer._regex_pattern == r'(\[Unreleased\]:[\s\S]+)'
