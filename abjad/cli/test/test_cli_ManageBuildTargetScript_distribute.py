import abjad
import os
import platform
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from unittest import mock
from uqbar.strings import normalize


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/distribution/.gitignore',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-cello.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-viola.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-violin-i.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-violin-ii.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-score.pdf',
    ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    @mock.patch('abjad.IOManager.open_file')
    def test_success(self, open_file_mock):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        self.install_fancy_segment_maker()
        pytest.helpers.create_segment(self.test_directory_path, 'test_segment')
        self.illustrate_segments()
        self.collect_segments()
        self.create_build_target()
        script = abjad.cli.ManageBuildTargetScript()
        command = ['--render', 'letter-portrait']
        with uqbar.io.DirectoryChange(self.score_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--distribute', 'letter-portrait']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''
            Distributing 'letter-portrait'
                score.pdf --> letter-portrait-score.pdf
                parts-cello.pdf --> letter-portrait-parts-cello.pdf
                parts-viola.pdf --> letter-portrait-parts-viola.pdf
                parts-violin-i.pdf --> letter-portrait-parts-violin-i.pdf
                parts-violin-ii.pdf --> letter-portrait-parts-violin-ii.pdf
            ''',
        )
        self.compare_path_contents(
            self.distribution_path,
            self.expected_files,
        )
