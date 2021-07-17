import os
from datetime import date

import click
import pyperclip
import questionary
from jinja2 import Environment, PackageLoader
from semver import VersionInfo
from .util import get_first_git_remote
from .changelog import Changelog


@click.group()
def cli():
    """
    A CLI tool for CHANGELOG files that follow the Keep-a-Changelog standard.
    """
    pass


@cli.command()
@click.option('-f', '--filename', 'filename', help='The filename of the CHANGELOG file to be created.',
              default=Changelog.default_file_name,
              type=click.Path(exists=True, dir_okay=False, writable=True, resolve_path=True), show_default=True)
def copy(filename):
    """Copy the latest release's changelog text."""
    changelog = Changelog(filename)
    pyperclip.copy(changelog.latest_release.changes_text)
    click.echo(f'v{changelog.latest_version} release text copied to clipboard!')


@cli.command()
@click.option('-f', '--filename', 'filename', help='The filename of the CHANGELOG file to be created.',
              default=Changelog.default_file_name,
              type=click.Path(exists=True, dir_okay=False, writable=True, resolve_path=True), show_default=True)
@click.option('-p', '--pre-release', 'prerelease', help='The prerelease identifier token.', default='rc',
              type=click.STRING, show_default=True)
@click.option('-b', '--build', 'build', help='The build identifier token.', default='build', type=click.STRING,
              show_default=True)
def bump(filename, build, prerelease):
    """Bump the latest version of a CHANGELOG file."""
    changelog = Changelog(filename)
    if not changelog.unreleased.has_changes:
        click.echo('CHANGELOG has no unreleased changes.')
        raise click.Abort

    available_versions = changelog.get_next_versions(prerelease, build)

    # Ask user to select new version
    new_v_num: str = questionary.select(
        message=f'Please select a new version (currently v{changelog.latest_version})',
        choices=[v_num for v_num in available_versions.keys()]
    ).ask()
    if new_v_num is None:
        raise click.Abort
    new_version = available_versions[new_v_num]
    # Confirm selected new version
    should_bump: bool = questionary.confirm(message=f'Bump Changelog to v{new_version}?').ask()
    # Bump or end
    if not should_bump:
        raise click.Abort

    changelog.bump(new_version)

    click.echo(f'Bumped to v{new_version}!')


@cli.command()
@click.option('-f', '--filename', 'filename', help='The filename of the CHANGELOG file to be created.',
              default=Changelog.default_file_name, type=click.Path(dir_okay=False, writable=True, resolve_path=True),
              show_default=True)
def init(filename):
    """Create an empty CHANGELOG file."""
    # Check if the file already exists
    if os.path.isfile(filename):
        click.echo(f'The CHANGELOG file already exists!')
        raise click.Abort

    # Ask the user for the initial version of their project
    first_v_num: str = questionary.text(
        message='Enter your first version number',
        default='0.0.1'
    ).ask()
    if first_v_num is None:
        raise click.Abort
    # Remove leading `v` if it exists
    if first_v_num[0] == 'v':
        first_v_num = first_v_num[1:]
    # Try to parse version using semver lib
    try:
        version = VersionInfo.parse(first_v_num)
    except ValueError:
        click.echo(f'Invalid Semantic Version number: {first_v_num}')
        raise click.Abort

    # Ask the user for their GitHub repository URL
    github_repo_url: str = questionary.text(
        message='Enter Repository URL',
        default=get_first_git_remote() or 'https://github.com/atwalsh/kac',
    ).ask()
    if github_repo_url is None:
        raise click.Abort

    # Load the CHANGELOG template
    env = Environment(loader=PackageLoader('kac', 'templates'), )
    changelog_template = env.get_template('CHANGELOG.md')
    # Render the template with user input
    new_file_text = changelog_template.render(initial_release=version, repo_url=github_repo_url,
                                              initial_release_date=date.today())

    # Write the new CHANGELOG file
    try:
        with click.open_file(filename, 'x') as f:  # `x` mode will fail to open if file exists
            f.write(new_file_text)
            click.echo(f'Created CHANGELOG file at: {filename}')
    except FileExistsError:
        click.echo('The CHANGELOG file already exists!')
        raise click.Abort
