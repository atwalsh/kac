from pathlib import Path
from unittest.mock import Mock

from click.testing import CliRunner

from kac.kac import init


class TestInit:
    def test_creation(self, monkeypatch):
        runner = CliRunner()
        expected_path = f'{Path(__file__).parent.parent.resolve()}/files/test_init_file.md'

        # Mock user prompts
        sf_mock = Mock()
        sf_mock.side_effect = ['0.0.1', 'https://github.com/atwalsh/kac']
        mock_text = Mock()
        mock_text.ask = sf_mock
        monkeypatch.setattr('questionary.text', lambda *args, **kwargs: mock_text)
        with runner.isolated_filesystem() as iso:
            res = runner.invoke(init, args=['-f', f'{iso}/CHANGELOG.md'])

            try:
                assert res.output == f'Created CHANGELOG file at: {iso}/CHANGELOG.md\n'
            except AssertionError:
                # For some reason, the path on macOS is prepended with `/private`
                assert res.output == f'Created CHANGELOG file at: /private{iso}/CHANGELOG.md\n'

            with open('CHANGELOG.md') as new_f, open(expected_path) as expected:
                assert new_f.read() == expected.read()
