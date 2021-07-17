import io
from unittest.mock import patch

from kac.util import get_first_git_remote


class TestUtil:
    def test_get_first_git_remote(self):
        test_config_data = '[remote "origin"]\n\turl = https://github.com/atwalsh/test.git' \
                           '\n\tfetch = +refs/heads/*:refs/remotes/origin/*'
        with patch("configparser.open") as mocked_open:
            mocked_open.return_value = io.StringIO(test_config_data)
            assert get_first_git_remote() == 'https://github.com/atwalsh/test'
