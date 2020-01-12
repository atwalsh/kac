import click
import questionary

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
