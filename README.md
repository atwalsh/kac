## kac
A command line tool for bumping Changelogs that follow the [Keep A Changelog][1] standard.

### Install
```bash
pip install kac
```

### Run
Run `kac` in the same directory as your Changelog, or pass the filepath as an argument. By default, `kac` looks for a 
file called `CHANGELOG.md` (case-insensitive).

### Example
Assuming you have a Changelog file at v3.6.2 name `CHANGELOG.md` in your current directory.

1. Run `kac`
    ```bash
    $ kac
    ```
2. Choose a bump version
    ```bash
    ? Please select a new version (currently v3.6.2)  (Use arrow keys)
       v3.6.3
     » v3.7.0
       v4.0.0
    ```
3. Confirm version bump (Y / Enter)
    ```bash
    ? Bump Changelog to v3.7.0? (Y/n)
    ```
4. Changelog bumped
   ```bash
   Changelog bumped to v3.7.0!
   ```
   
## Limitations
- Assumes you have changes in the "Unreleased" section 
- Only works for semver
- Only supports versions in the `MAJOR.MINOR.PATCH` format. A beta version ending in `-beta`, for example, 
will fail.

## To-Do
- [ ] Add tests
- [ ] Add support for generating an empty Changelog template
- [ ] Undo bump
- [ ] Support labels for pre-release and build metadata

[1]: https://keepachangelog.com/en/1.0.0/