from .section import Section


class Footer(Section):
    """
    Represents the footer section of the Changelog, consisting of all text before the Body section.
    """
    _regex_pattern = r'(\[Unreleased\]:[\s\S]+)'
