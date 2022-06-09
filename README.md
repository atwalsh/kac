# kac

Python and CLI tool for CHANGELOG files that follow the [Keep a Changelog][1] standard.

## Installation

```console
pip install kac
```

## CLI

Run `kac` in the same directory as your Changelog. By default, `kac` looks for a file called `CHANGELOG.md`
(case-insensitive).

```console
Usage: kac [OPTIONS] COMMAND [ARGS]...

  Python and  CLI tool for CHANGELOG files that follow the Keep a Changelog
  standard.

Options:
  --help  Show this message and exit.

Commands:
  bump  Bump the latest version of a CHANGELOG file.
  copy  Copy the latest release's changelog text.
  init  Create an empty CHANGELOG file.

```

## API

### Changelog

Create a `Changelog` object:
```python
>>> from kac.changelog import Changelog
>>> Changelog('CHANGELOG.md')
<CHANGELOG v0.5.0>
```

Interact with a `Changelog`:
```python
>>> from kac.changelog import Changelog
>>> changelog = Changelog('/path/to/CHANGELOG.md')
>>> changelog.latest_version
VersionInfo(major=0, minor=5, patch=0, prerelease=None, build=None)

>>> changelog.latest_release
<Release v0.5.0 - 2021-09-11>

>>> changelog.latest_release.added # Get a list of changes for latest release
['`-t/--type` option for `bump` command']
```
## Limitations

- Must be run in the same directory as your CHANGELOG file
- Only works for semver
- `kac bump` can "format" (ex: remove extra empty lines) CHANGELOG files, this could be unfavorable for users

[1]: https://keepachangelog.com/en/1.0.0/