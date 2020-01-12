## kac
A command line tool for CHANGELOG files that follow the [Keep A Changelog][1] standard.

### Usage
Run `kac` in the same directory as your Changelog. By default, `kac` looks for a file called `CHANGELOG.md` 
(case-insensitive).

```bash
Usage: kac [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  bump  Bump a Changelog.
  copy  Copy a version's release text.
```

## Limitations
- Must be run in the same directory as your CHANGELOG file
- Assumes you have changes in the "Unreleased" section 
- Only works for semver
- Only supports versions in the `MAJOR.MINOR.PATCH` format. A beta version ending in `-beta`, for example, 
will fail.

## To-Do
- [ ] Add default text for versions with no notable changes
- [ ] Add tests
- [ ] Add support for generating an empty Changelog template
- [ ] Undo bump
- [ ] Support labels for pre-release and build metadata

[1]: https://keepachangelog.com/en/1.0.0/