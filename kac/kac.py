import os

import click
import questionary
from jinja2 import Environment, PackageLoader
from semver import parse_version_info as semver_parse

from .changelog import Changelog
from .changelog.util import parse_version_number


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True), default=Changelog.default_file_name)
@click.option('-v', '--version', 'version', default=Changelog.LATEST, required=True)
def copy(filename, version):
    """Copy a version's release text."""
    c = Changelog(filename)
    v = version
    if v != Changelog.LATEST:
        try:
            v = parse_version_number(version)
        except ValueError as e:
            raise click.UsageError(str(e))
    c.copy_release_text(v)


@cli.command()
@click.argument('filename', type=click.Path(exists=True), default=Changelog.default_file_name)
def bump(filename):
    """Bump a Changelog."""
    c = Changelog(filename)
    # Ask user to select new version
    new_v_num: str = questionary.select(
        message=f'Please select a new version (currently v{c.major}.{c.minor}.{c.patch})',
        choices=[v_num for v_num in c.available_new_versions.keys()]
    ).ask()
    if new_v_num is None:
        raise click.Abort
    # Confirm selected new version
    should_bump: bool = questionary.confirm(
        message=f'Bump Changelog to v{new_v_num}?'
    ).ask()
    # Bump or end
    if not should_bump:
        raise click.Abort
    c.bump(c.available_new_versions[new_v_num])
    click.echo(f'Bumped to v{new_v_num}!')


@cli.command()
@click.option('-f', '--filename', 'filename', help='The filename of the CHANGELOG file to be created.',
              default=Changelog.default_file_name_upper, type=click.Path(dir_okay=False, writable=True),
              show_default=True)
def init(filename: click.File):
    """Create an empty CHANGELOG file."""
    # Check if the file already exists
    full_path = os.path.realpath(click.format_filename(filename))
    if os.path.isfile(full_path):
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
        version = semver_parse(first_v_num)
    except ValueError:
        click.echo(f'Invalid Semantic Version number: {first_v_num}')
        raise click.Abort

    # Ask the user for their GitHub repository URL
    github_repo_url: str = questionary.text(
        message='Enter Repository URL',
        default='https://github.com/atwalsh/kac',
    ).ask()
    if github_repo_url is None:
        raise click.Abort

    # Load the CHANGELOG template
    env = Environment(loader=PackageLoader('kac', 'templates'), )
    changelog_template = env.get_template('CHANGELOG.md')
    # Render the template with user input
    new_file_text = changelog_template.render(initial_release=version, repo_url=github_repo_url)

    # Write the new CHANGELOG file
    try:
        with click.open_file(full_path, 'x') as f:  # `x` mode will fail to open if file exists
            f.write(new_file_text)
            click.echo(f'Created CHANGELOG file at: {full_path}')
    except FileExistsError:
        click.echo('The CHANGELOG file already exists!')
        raise click.Abort
