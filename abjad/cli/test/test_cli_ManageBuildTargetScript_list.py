import abjad
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from uqbar.strings import normalize


class Test(ScorePackageScriptTestCase):

    def test_list(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        script = abjad.cli.ManageBuildTargetScript()
        command = ['--new', 'big-version']
        with uqbar.io.DirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'medium-version']
        with uqbar.io.DirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'small-version']
        with uqbar.io.DirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--list']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        assert normalize(string_io.getvalue()) == normalize(r'''
        Available build targets:
            big-version
            medium-version
            small-version
        ''')
