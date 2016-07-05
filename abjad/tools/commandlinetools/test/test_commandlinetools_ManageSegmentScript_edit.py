# -*- coding: utf-8 -*-
import os
from abjad import abjad_configuration
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase
try:
    from unittest import mock
except ImportError:
    import mock


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.commandlinetools.ScorePackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        self.create_score()
        segment_path = self.create_segment('test_segment')
        script = commandlinetools.ManageSegmentScript()
        command = ['--edit', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Edit candidates: 'test_segment' ...
            Reading test_score/segments/metadata.json ... OK!
        '''.replace('/', os.path.sep))
        definition_path = segment_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            abjad_configuration.get_text_editor(),
            definition_path,
            )
        call_subprocess_mock.assert_called_with(command)
