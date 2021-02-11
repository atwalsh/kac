import re
from collections import OrderedDict
from datetime import date
from typing import List

import click
from semver import VersionInfo


class ReleaseBase:
    """
    Represents a release in a Changelog file.
    """
    _change_pattern = re.compile(r'^### (\S+)$\n+((?:^- (?:.*)$\n)+)\s*')

    CHANGE_TYPES = (
        'added',
        'changed',
        'deprecated',
        'fixed',
        'removed',
        'security',
    )

    def __init__(self, added: List = None, changed: List = None, deprecated: List = None, fixed: List = None,
                 removed: List = None, security: List = None):
        if added is None:
            added = []
        if changed is None:
            changed = []
        if deprecated is None:
            deprecated = []
        if fixed is None:
            fixed = []
        if removed is None:
            removed = []
        if security is None:
            security = []

        self.added = added
        self.changed = changed
        self.deprecated = deprecated
        self.fixed = fixed
        self.removed = removed
        self.security = security

        self.changes: OrderedDict = OrderedDict([
            ('added', self.added),
            ('changed', self.changed),
            ('deprecated', self.deprecated),
            ('fixed', self.fixed),
            ('removed', self.removed),
            ('security', self.security),
        ])

    @classmethod
    def changes_to_dict(cls, changes_text) -> dict:
        """
        Parse a release's changes into a dictionary where keys are the change type (ie. Added => `added` key), and
        values are a list of changes for that change type.

        :raises click.Abort: If change type is not in CHANGE_TYPES.

        :param changes_text: Text of changes from a release.
        :return: Dictionary of change types and changes.
        """
        data = {v: [] for v in cls.CHANGE_TYPES}
        for change_type, change_data in re.findall(r'### (\S+)\n+((?:- (?:.*)\n*)+)\s*',
                                                   changes_text.strip()):  # type: str, str
            change_data = change_data.strip()
            if change_type.lower() not in Release.CHANGE_TYPES:
                click.echo(f'Invalid change type: {change_type}')
                raise click.Abort
            data[change_type.lower()].extend([cd.lstrip('- ') for cd in change_data.split('\n')])
        return data

    @property
    def changes_text(self):
        data = ''
        for change_type, change_data in self.changes.items():  # type: str, str
            if not change_data:
                continue
            change_entries = ''.join([f'- {cd}\n' for cd in change_data])
            data += f'### {change_type.capitalize()}\n{change_entries}\n'

        return data


class Release(ReleaseBase):
    def __init__(self, version: VersionInfo, release_date: date, added: List = None, changed: List = None,
                 deprecated: List = None, fixed: List = None, removed: List = None, security: List = None):
        super(Release, self).__init__(added, changed, deprecated, removed, fixed, security)
        self.release_date = release_date
        self.version = version

    def __repr__(self):
        return f'<Release v{self.version} - {self.release_date}>'

    def __eq__(self, other):
        return self.version == other.version and self.release_date == other.release_date


class Unreleased(ReleaseBase):
    def __repr__(self):
        return '<Unreleased>'

    @property
    def has_changes(self):
        return any(cv for cv in self.changes.values())
