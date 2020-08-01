from .section import Section


class Footer(Section):
    """
    Represents the footer section of the Changelog - consisting of all text before the Body section, usually URL
    references to release tags.
    """
    _regex_pattern = r'(\[Unreleased\]:[\s\S]+)'
