# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Something added

### Changed
- `template` command to `new`

## [0.3.0] - 2020-04-05
### Added
- `template` command
- Initial basic tests with SemaphoreCI integration
- Automatic releases to PyPI on git tags

### Changed
- Use poetry instead of pipenv

## [0.2.3] - 2020-03-19
### Fixed
- Issue where extra newline characters were copied to the clipboard

## [0.2.2] - 2020-01-14
### Fixed
- Issue where `bump` would not properly show the latest version 

## [0.2.1] - 2020-01-11
### Fixed
- Issue where `copy` would not correctly copy release text with new lines

## [0.2.0] - 2020-01-11
### Added
- `bump` and `copy` commands

### Changed
- `kac` cannot be invoked without either the `bump` or `copy` commands

## [0.1.3] - 2019-11-20
### Removed
- Python 3.8 walrus operators

## [0.1.2] - 2019-11-14
### Fixed
- Bug where `v` character would not be added to end of version compare URL

## [0.1.1] - 2019-11-14
### Added
- `install_requires` argument in setup.py

## [0.1.0] - 2019-11-14
### Added
- This Changelog and initial project files

[Unreleased]: https://github.com/atwalsh/kac/compare/v0.3.0...master
[0.3.0]: https://github.com/atwalsh/kac/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/atwalsh/kac/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/atwalsh/kac/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/atwalsh/kac/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/atwalsh/kac/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/atwalsh/kac/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/atwalsh/kac/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/atwalsh/kac/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/atwalsh/kac/releases/tag/v0.1.0
