from pathlib import Path
from unittest.mock import Mock

from click.testing import CliRunner
from freezegun import freeze_time

from kac.kac import bump


class TestBump:
    @freeze_time('2021-01-16')
    def test_no_args(self, test_changelog_path, monkeypatch):
        runner = CliRunner()
        bumped_path = f'{Path(__file__).parent.parent.resolve()}/files/test_changelog_file_bumped.md'

        # Mock user prompts
        mock_select = Mock()
        mock_select.ask.return_value = 'v0.4.0'
        monkeypatch.setattr('questionary.select', lambda *args, **kwargs: mock_select)
        mock_confirm = Mock()
        mock_confirm.ask = lambda *args, **kwargs: True
        monkeypatch.setattr('questionary.confirm', lambda *args, **kwargs: mock_confirm)

        with open(test_changelog_path) as f:
            text = f.read()
        with runner.isolated_filesystem():
            with open('CHANGELOG.md', 'w') as new_f:
                new_f.write(text)

            res = runner.invoke(bump, input='\n'.join(['']))
            assert res.output == 'Bumped to v0.4.0!\n'

            with open('CHANGELOG.md') as mod_f, open(bumped_path) as expected:
                assert mod_f.read() == expected.read()
