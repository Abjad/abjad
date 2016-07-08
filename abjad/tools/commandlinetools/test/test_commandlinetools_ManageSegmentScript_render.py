# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase
try:
    from unittest import mock
except ImportError:
    import mock


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/segments/.gitignore',
        'test_score/test_score/segments/__init__.py',
        'test_score/test_score/segments/metadata.json',
        'test_score/test_score/segments/test_segment/__init__.py',
        'test_score/test_score/segments/test_segment/definition.py',
        'test_score/test_score/segments/test_segment/illustration.ly',
        'test_score/test_score/segments/test_segment/illustration.pdf',
        'test_score/test_score/segments/test_segment/metadata.json',
        ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_one_segment(self, open_file_mock):
        self.create_score()
        segment_path = self.create_segment('test_segment')
        self.illustrate_segment('test_segment')
        pdf_path = segment_path.joinpath('illustration.pdf')
        assert pdf_path.exists()
        pdf_path.unlink()
        script = commandlinetools.ManageSegmentScript()
        command = ['--render', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Rendering candidates: 'test_segment' ...
            Reading test_score/segments/metadata.json ... OK!
        Rendering test_score/segments/test_segment/
            Writing test_score/segments/test_segment/illustration.pdf ... OK!
                LilyPond runtime: ... second...
            Rendered test_score/segments/test_segment/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.segments_path, self.expected_files)
