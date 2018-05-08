import abjad
import os
import platform
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from unittest import mock


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

    @mock.patch('abjad.IOManager.open_file')
    def test_success_one_segment(self, open_file_mock):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        segment_path = pytest.helpers.create_segment(
            self.test_directory_path, 'test_segment')
        self.illustrate_segment('test_segment')
        pdf_path = segment_path.joinpath('illustration.pdf')
        assert pdf_path.exists()
        pdf_path.unlink()
        script = abjad.cli.ManageSegmentScript()
        command = ['--render', 'test_segment']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            expected=r'''
            Rendering candidates: 'test_segment' ...
                Reading test_score/segments/metadata.json ... OK!
            Rendering test_score/segments/test_segment/
                Writing test_score/segments/test_segment/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Rendered test_score/segments/test_segment/
            '''.replace('/', os.path.sep),
            actual=string_io.getvalue(),
        )
        self.compare_path_contents(self.segments_path, self.expected_files)
