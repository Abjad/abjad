import abjad
import os
import pytest
import uqbar.io
from abjad import abjad_configuration
from base import ScorePackageScriptTestCase
from io import StringIO
from unittest import mock
from uqbar.strings import normalize


class Test(ScorePackageScriptTestCase):

    def side_effect(self, command, **keywords):
        _, file_name = command.split()
        contents = normalize('''
        segment_c
        segment_b
        segment_a
        ''')
        with open(file_name, 'w') as file_pointer:
            file_pointer.write(contents)

    @mock.patch('abjad.cli.ScorePackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        string_io = StringIO()
        call_subprocess_mock.return_value = 0
        pytest.helpers.create_score(self.test_directory_path)
        pytest.helpers.create_segment(self.test_directory_path, 'segment_a')
        pytest.helpers.create_segment(self.test_directory_path, 'segment_b')
        pytest.helpers.create_segment(self.test_directory_path, 'segment_c')
        script = abjad.cli.ManageSegmentScript()
        command = ['--stage']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''
            Staging segments:
                Reading test_score/segments/metadata.json ... OK!
            Staged:
                segment_a
                segment_b
                segment_c
            '''.replace('/', os.path.sep),
        )
        call_subprocess_mock.assert_called_with(
            '{} segments.txt'.format(abjad_configuration.get_text_editor()),
        )
        call_subprocess_mock.side_effect = self.side_effect
        string_io = StringIO()
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''
            Staging segments:
                Reading test_score/segments/metadata.json ... OK!
                Writing test_score/segments/metadata.json
            Staged:
                segment_c
                segment_b
                segment_a
            '''.replace('/', os.path.sep),
        )
        call_subprocess_mock.assert_called_with(
            '{} segments.txt'.format(abjad_configuration.get_text_editor()),
        )
