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
        'test_score/test_score/distribution/.gitignore',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-cello.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-viola.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-violin-i.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-violin-ii.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-score.pdf',
        ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success(self, open_file_mock):
        self.create_score()
        self.install_fancy_segment_maker()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--render', 'letter-portrait']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--distribute', 'letter-portrait']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Distributing 'letter-portrait'
            score.pdf --> letter-portrait-score.pdf
            parts-cello.pdf --> letter-portrait-parts-cello.pdf
            parts-viola.pdf --> letter-portrait-parts-viola.pdf
            parts-violin-i.pdf --> letter-portrait-parts-violin-i.pdf
            parts-violin-ii.pdf --> letter-portrait-parts-violin-ii.pdf
        ''')
        self.compare_path_contents(
            self.distribution_path,
            self.expected_files,
            )
