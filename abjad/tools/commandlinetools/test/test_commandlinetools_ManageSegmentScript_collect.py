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
        'test_score/test_score/build/.gitignore',
        'test_score/test_score/build/assets/.gitignore',
        'test_score/test_score/build/assets/instrumentation.tex',
        'test_score/test_score/build/assets/performance-notes.tex',
        'test_score/test_score/build/parts.ily',
        'test_score/test_score/build/segments.ily',
        'test_score/test_score/build/segments/.gitignore',
        'test_score/test_score/build/segments/segment-one.ily',
        'test_score/test_score/build/segments/segment-three.ily',
        'test_score/test_score/build/segments/segment-two.ily',
        ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success(self, open_file_mock):
        self.create_score()
        self.create_segment('segment_one')
        self.create_segment('segment_two')
        self.create_segment('segment_three')
        self.illustrate_segments()
        collect_script = commandlinetools.ManageSegmentScript()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    collect_script(['--collect'])
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Collecting segments:
            segments/segment_one/illustration.ly --> build/segments/segment-one.ily
            segments/segment_three/illustration.ly --> build/segments/segment-three.ily
            segments/segment_two/illustration.ly --> build/segments/segment-two.ily
            Reading test_score/segments/metadata.json ... OK!
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.build_path, self.expected_files)
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
