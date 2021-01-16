![kac](https://atw.me/img/kac.svg)

<hr>

A command line tool for CHANGELOG files that follow the [Keep A Changelog][1] standard.

![Tests](https://github.com/atwalsh/kac/workflows/Tests/badge.svg)

### Usage

Run `kac` in the same directory as your Changelog. By default, `kac` looks for a file called `CHANGELOG.md`
(case-insensitive).

```
Usage: kac [OPTIONS] COMMAND [ARGS]...

  A CLI tool for CHANGELOG files that follow the Keep-a-Changelog standard.

Options:
  --help  Show this message and exit.

Commands:
  bump  Bump the latest version of a CHANGELOG file.
  copy  Copy the latest release's changelog text.
  init  Create an empty CHANGELOG file.
  
```

## Limitations

- Must be run in the same directory as your CHANGELOG file
- Only works for semver

[1]: https://keepachangelog.com/en/1.0.0/