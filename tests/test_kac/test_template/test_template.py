import os
from pathlib import Path
from unittest.mock import patch, Mock

from click.testing import CliRunner
from prompt_toolkit.application.current import AppSession
from prompt_toolkit.input import DummyInput
from prompt_toolkit.output import DummyOutput
from questionary.question import Question

from kac.changelog import Changelog
from kac.kac import template


def test_file_exists():
    """
    Test that the template command exists if a CHANGELOG file already exists.
    """
    r_1_filename = Changelog.default_file_name  # changelog.md
    r_2_filename = r_1_filename.capitalize()  # Changelog.md
    r_3_filename = r_1_filename.upper()  # CHANGELOG.md
    test_filenames = (r_1_filename, r_2_filename, r_3_filename,)
    runner = CliRunner()
    with runner.isolated_filesystem() as _dir:
        for idx, f_name in enumerate(test_filenames):
            if idx > 0:
                os.remove(f'{_dir}/{test_filenames[idx - 1]}')
            assert [f for f in os.listdir('.') if os.path.isfile(f)] == []
            Path(f'{_dir}/{f_name}').touch()
            res = runner.invoke(template)
            assert res.exit_code == 1
            assert res.output == 'A CHANGELOG file already exists.\nAborted!\n'


def test_create_template_v0_0_1(monkeypatch):
    """
    Test that we can successfully create a empty v0.0.1 CHANGELOG template.
    """
    monkeypatch.setattr(AppSession, 'output', DummyOutput())
    monkeypatch.setattr(AppSession, 'input', DummyInput())
    runner = CliRunner()
    with open(f'{Path(__file__).parent.resolve()}/templates/changelog-v0-0-1.md', 'r') as exp_f:
        expected_file_text = exp_f.read()
    with runner.isolated_filesystem() as _dir:
        mock_res = Mock()
        mock_res.side_effect = ['0.0.1', 'https://github.com/atwalsh/kac']
        patch('questionary.prompts.text.text', mock_res)
        monkeypatch.setattr(Question, 'ask', mock_res)
        res = runner.invoke(template)
        assert res.exit_code == 0
        assert [f for f in os.listdir('.') if os.path.isfile(f)] == [Changelog.default_file_name_upper]
        with open(f'{_dir}/{Changelog.default_file_name_upper}') as act_f:
            assert act_f.read() == expected_file_text
