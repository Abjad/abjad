# -*- coding: utf-8 -*-
import os
from abjad import abjad_configuration
from abjad.tools import commandlinetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase
try:
    from unittest import mock
except ImportError:
    import mock


class Test(ScorePackageScriptTestCase):

    def side_effect(self, command, **kwargs):
        _, file_name = command.split()
        contents = stringtools.normalize('''
        segment_c
        segment_b
        segment_a
        ''')
        with open(file_name, 'w') as file_pointer:
            file_pointer.write(contents)

    @mock.patch('abjad.commandlinetools.ScorePackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        self.create_score()
        self.create_segment('segment_a')
        self.create_segment('segment_b')
        self.create_segment('segment_c')
        script = commandlinetools.ManageSegmentScript()
        command = ['--stage']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Staging segments:
            Reading test_score/segments/metadata.json ... OK!
        Staged:
            segment_a
            segment_b
            segment_c
        '''.replace('/', os.path.sep))
        call_subprocess_mock.assert_called_with(
            '{} segments.txt'.format(abjad_configuration.get_text_editor()),
            )
        call_subprocess_mock.side_effect = self.side_effect
        self.reset_string_io()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Staging segments:
            Reading test_score/segments/metadata.json ... OK!
            Writing test_score/segments/metadata.json
        Staged:
            segment_c
            segment_b
            segment_a
        '''.replace('/', os.path.sep))
        call_subprocess_mock.assert_called_with(
            '{} segments.txt'.format(abjad_configuration.get_text_editor()),
            )
