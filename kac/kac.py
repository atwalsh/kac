import click
import questionary

from .changelog import Changelog


@click.command()
@click.argument('filename', type=click.Path(exists=True), default=Changelog.default_file_name)
def main(filename):
    c = Changelog(filename)
    # Ask user to select new version
    new_v_num: str = questionary.select(
        message=f'Please select a new version (currently v{c.major}.{c.minor}.{c.patch})',
        choices=[v_num for v_num in c.available_new_versions.keys()]
    ).ask()
    if new_v_num is None:
        end()
    # Confirm selected new version
    should_bump: bool = questionary.confirm(
        message=f'Bump Changelog to v{new_v_num}?'
    ).ask()
    # Bump or end
    c.bump(c.available_new_versions[new_v_num]) if should_bump is True else end()
    click.echo(f'Bumped to v{new_v_num}!')


def end():
    """Exit."""
    print('Not bumping Changelog.')
    exit()
