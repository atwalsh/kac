import configparser
import re


def get_first_git_remote() -> str:
    """
    Attempt to get the first git remote URL from the ./.git/config file in the current directory.
    :return: URL for the first git remote or an empty string if a remote URL could not be identified.
    """
    git_config = configparser.ConfigParser()
    try:
        files = git_config.read('./.git/config')
    except configparser.Error:
        return ''
    if not files or len(files) > 1:  # ConfigParser.read() returns a list of successfully read files
        return ''

    for section in git_config.sections():
        if section.startswith('remote'):
            remote = git_config[section].get('url')
            return re.sub(r'\.git$', '', remote)
