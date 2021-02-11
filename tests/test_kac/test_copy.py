from click.testing import CliRunner

from kac.kac import copy


class TestCopy:
    def test_no_args(self, test_changelog_path):
        runner = CliRunner()
        with open(test_changelog_path) as f:
            text = f.read()
        with runner.isolated_filesystem():
            with open('CHANGELOG.md', 'w') as new_f:
                new_f.write(text)

            res = runner.invoke(copy)
            assert res.exit_code == 0
            assert res.output == 'v0.3.0 release text copied to clipboard!\n'

    def test_filename_arg(self, test_changelog_path):
        runner = CliRunner()
        with open(test_changelog_path) as f:
            text = f.read()
        with runner.isolated_filesystem() as iso:
            with open('CHANGELOG.md', 'w') as new_f:
                new_f.write(text)

            res = runner.invoke(copy, ['-f', iso + '/CHANGELOG.md'])
            assert res.exit_code == 0
            assert res.output == 'v0.3.0 release text copied to clipboard!\n'

    def test_bad_filename_arg(self):
        runner = CliRunner()
        with runner.isolated_filesystem() as iso:
            res = runner.invoke(copy, ['-f', iso + '/CHANGELOG.md'])  # Does not exist
            assert res.exit_code == 2
            assert res.output == f"Usage: copy [OPTIONS]\n" \
                                 f"Try 'copy --help' for help.\n\n" \
                                 f"Error: Invalid value for \'-f\' / \'--filename\': " \
                                 f"File \'{iso}/CHANGELOG.md\' does not exist.\n"
