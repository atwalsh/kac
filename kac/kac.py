import os

import click
import questionary
from jinja2 import Environment, PackageLoader

from .changelog import Changelog


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
            v = Changelog.parse_version_number(version)
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
def template():
    """Create an empty CHANGELOG.md file."""
    # Fail if a CHANGELOG.md already exists
    if (len([filename for filename in os.listdir(os.getcwd()) if
             filename.lower() == Changelog.default_file_name.lower()])) != 0:
        click.echo(f'A CHANGELOG file already exists.')
        raise click.Abort
    # Ask the user for the initial version of their project
    first_v_num: str = questionary.text(
        message='Enter your first version number',
        default='0.0.1'
    ).ask()
    if first_v_num is None:
        raise click.Abort
    # Ask the user for their GitHub repository URL
    github_repo_url: str = questionary.text(
        message='Enter Repository URL',
        default='https://github.com/atwalsh/kac'
    ).ask()
    if github_repo_url is None:
        raise click.Abort
    # Load the CHANGELOG template
    env = Environment(loader=PackageLoader('kac', 'templates'), )
    changelog_template = env.get_template('CHANGELOG.md')
    # Render the template with user input
    new_file_text = changelog_template.render(initial_release=first_v_num, repo_url=github_repo_url)
    # White the new file
    with open(Changelog.default_file_name_upper, 'w') as f:
        f.write(new_file_text)
        click.echo(f'Created {Changelog.default_file_name_upper} file at: {os.path.realpath(f.name)}')
