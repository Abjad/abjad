import abjad
import pytest
from base import ScorePackageScriptTestCase
from io import StringIO


class Test(ScorePackageScriptTestCase):

    def test_list(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        script = abjad.cli.ManageBuildTargetScript()
        command = ['--new', 'big-version']
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'medium-version']
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'small-version']
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--list']
        with abjad.RedirectedStreams(stdout=string_io):
            with abjad.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Available build targets:
            big-version
            medium-version
            small-version
        ''')
