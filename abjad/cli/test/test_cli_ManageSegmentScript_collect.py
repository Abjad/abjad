import abjad
import os
import platform
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from unittest import mock


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.IOManager.open_file')
    def test_success(self, open_file_mock):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        pytest.helpers.create_segment(self.test_directory_path, 'segment_one')
        pytest.helpers.create_segment(self.test_directory_path, 'segment_two')
        pytest.helpers.create_segment(
            self.test_directory_path, 'segment_three')
        self.illustrate_segments()
        collect_script = abjad.cli.ManageSegmentScript()
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    collect_script(['--collect'])
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''
            Collecting segments:
                segments/segment_one/illustration.ly --> builds/segments/segment-one.ily
                segments/segment_three/illustration.ly --> builds/segments/segment-three.ily
                segments/segment_two/illustration.ly --> builds/segments/segment-two.ily
                Reading test_score/segments/metadata.json ... OK!
            '''.replace('/', os.path.sep),
        )
        expected_files = [
            'test_score/test_score/builds/.gitignore',
            'test_score/test_score/builds/assets/.gitignore',
            'test_score/test_score/builds/assets/instrumentation.tex',
            'test_score/test_score/builds/assets/performance-notes.tex',
            'test_score/test_score/builds/parts.ily',
            'test_score/test_score/builds/segments.ily',
            'test_score/test_score/builds/segments/.gitignore',
            'test_score/test_score/builds/segments/segment-one.ily',
            'test_score/test_score/builds/segments/segment-three.ily',
            'test_score/test_score/builds/segments/segment-two.ily',
        ]
        if platform.system().lower() == 'windows':
            expected_files = [
                _.replace('/', os.path.sep)
                for _ in expected_files
            ]
        self.compare_path_contents(self.build_path, expected_files)
        path = self.build_path.joinpath('segments.ily')
        self.compare_lilypond_contents(path, r'''
        {
            \include "../segments/segment-one.ily"
            \include "../segments/segment-two.ily"
            \include "../segments/segment-three.ily"
        }
        '''.replace('/', os.path.sep))
        path = self.build_path.joinpath('segments', 'segment-one.ily')
        self.compare_lilypond_contents(path, r'''
        \context Score = "Example Score" <<
            \context Staff = "Example Staff" {
                \context Voice = "Example Voice" {
                    c'4 (
                    d'4
                    e'4
                    f'4 )
                }
            }
        >>
        ''')
        path = self.build_path.joinpath('segments', 'segment-two.ily')
        self.compare_lilypond_contents(path, r'''
        \context Score = "Example Score" <<
            \context Staff = "Example Staff" {
                \context Voice = "Example Voice" {
                    c'4 (
                    d'4
                    e'4
                    f'4 )
                }
            }
        >>
        ''')
        path = self.build_path.joinpath('segments', 'segment-three.ily')
        self.compare_lilypond_contents(path, r'''
        \context Score = "Example Score" <<
            \context Staff = "Example Staff" {
                \context Voice = "Example Voice" {
                    c'4 (
                    d'4
                    e'4
                    f'4 )
                }
            }
        >>
        ''')
