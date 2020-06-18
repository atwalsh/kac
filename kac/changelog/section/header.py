from .section import Section


class Header(Section):
    """
    Represents the header section of the Changelog, consisting of all text before the `Unreleased` release text.
    """
    _regex_pattern = r'([\s\S]+)## \[Unreleased\]'
