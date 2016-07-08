# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import stringtools
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

    expected_illustration_contents = stringtools.normalize(
        r'''
        \language "english"

        \include "../../stylesheets/stylesheet.ily"

        \header {}

        \layout {}

        \paper {}

        \score {
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
        }
        ''')

    def test_lilypond_error(self):
        """
        Handle failing LilyPond rendering.
        """
        self.create_score()
        segment_path = self.create_segment('test_segment')
        definition_path = segment_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-
            from abjad.tools import abctools
            from abjad.tools import lilypondfiletools
            from abjad.tools import scoretools


            class FaultySegmentMaker(abctools.AbjadObject):

                def __call__(
                    self,
                    segment_metadata=None,
                    previous_segment_metadata=None,
                    ):
                    lilypond_file = lilypondfiletools.make_basic_lilypond_file(
                        scoretools.Staff("c'4 ( d'4 e'4 f'4 )")
                        )
                    lilypond_file.items.append(r'\this-does-not-exist')
                    return lilypond_file, segment_metadata

            segment_maker = FaultySegmentMaker()
            '''))
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_segment' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/test_segment/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/test_segment/metadata.json ... JSON does not exist.
                Importing test_score.segments.test_segment.definition
                Writing test_score/segments/test_segment/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/test_segment/illustration.ly ... OK!
                Writing test_score/segments/test_segment/illustration.pdf ... Failed!
        '''.replace('/', os.path.sep))
        illustration_ly_path = segment_path.joinpath('illustration.ly')
        assert illustration_ly_path.exists()
        self.compare_lilypond_contents(
            illustration_ly_path, stringtools.normalize(r'''
            \language "english"

            \header {}

            \layout {}

            \paper {}

            \score {
                \new Staff {
                    c'4 (
                    d'4
                    e'4
                    f'4 )
                }
            }

            \this-does-not-exist
            '''))

    def test_missing_definition(self):
        """
        Handle missing definition.
        """
        self.create_score()
        segment_path = self.create_segment('test_segment')
        definition_path = segment_path.joinpath('definition.py')
        definition_path.unlink()
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_segment' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/test_segment/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/test_segment/metadata.json ... JSON does not exist.
                Importing test_score.segments.test_segment.definition
        '''.replace('/', os.path.sep))

    def test_python_error_on_illustrate(self):
        """
        Handle exceptions inside the Python module on __call__().
        """
        self.create_score()
        segment_path = self.create_segment('test_segment')
        definition_path = segment_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-
            from abjad.tools import abctools


            class FaultySegmentMaker(abctools.AbjadObject):

                def __call__(
                    self,
                    segment_metadata=None,
                    previous_segment_metadata=None,
                    ):
                    raise TypeError('This is intentionally broken.')

            segment_maker = FaultySegmentMaker()
            '''))
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_segment' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/test_segment/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/test_segment/metadata.json ... JSON does not exist.
                Importing test_score.segments.test_segment.definition
        '''.replace('/', os.path.sep))

    def test_python_error_on_import(self):
        """
        Handle exceptions inside the Python module on import.
        """
        self.create_score()
        segment_path = self.create_segment('test_segment')
        definition_path = segment_path.joinpath('definition.py')
        with open(str(definition_path), 'a') as file_pointer:
            file_pointer.write('\n\nfailure = 1 / 0\n')
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_segment' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/test_segment/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/test_segment/metadata.json ... JSON does not exist.
                Importing test_score.segments.test_segment.definition
        '''.replace('/', os.path.sep))

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_all_segments(self, open_file_mock):
        self.create_score()
        self.create_segment('segment_one')
        self.create_segment('segment_two')
        self.create_segment('segment_three')
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', '*']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
            Illustration candidates: '*' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/segment_one/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/segment_one/metadata.json ... JSON does not exist.
                Importing test_score.segments.segment_one.definition
                Writing test_score/segments/segment_one/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/segment_one/illustration.ly ... OK!
                Writing test_score/segments/segment_one/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/segments/segment_one/
            Illustrating test_score/segments/segment_two/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/segment_one/metadata.json ... OK!
                Reading test_score/segments/segment_two/metadata.json ... JSON does not exist.
                Importing test_score.segments.segment_two.definition
                Writing test_score/segments/segment_two/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/segment_two/illustration.ly ... OK!
                Writing test_score/segments/segment_two/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/segments/segment_two/
            Illustrating test_score/segments/segment_three/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/segment_two/metadata.json ... OK!
                Reading test_score/segments/segment_three/metadata.json ... JSON does not exist.
                Importing test_score.segments.segment_three.definition
                Writing test_score/segments/segment_three/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/segment_three/illustration.ly ... OK!
                Writing test_score/segments/segment_three/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/segments/segment_three/
        '''.replace('/', os.path.sep))
        assert self.segments_path.joinpath(
            'segment_one',
            'illustration.pdf',
            ).exists()
        assert self.segments_path.joinpath(
            'segment_two',
            'illustration.pdf',
            ).exists()
        assert self.segments_path.joinpath(
            'segment_three',
            'illustration.pdf',
            ).exists()

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_filtered_segments(self, open_file_mock):
        self.create_score()
        self.create_segment('segment_one')
        self.create_segment('segment_two')
        self.create_segment('segment_three')
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', 'segment_t*']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
            Illustration candidates: 'segment_t*' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/segment_two/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/segment_one/metadata.json ... JSON does not exist.
                Reading test_score/segments/segment_two/metadata.json ... JSON does not exist.
                Importing test_score.segments.segment_two.definition
                Writing test_score/segments/segment_two/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/segment_two/illustration.ly ... OK!
                Writing test_score/segments/segment_two/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/segments/segment_two/
            Illustrating test_score/segments/segment_three/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/segment_two/metadata.json ... OK!
                Reading test_score/segments/segment_three/metadata.json ... JSON does not exist.
                Importing test_score.segments.segment_three.definition
                Writing test_score/segments/segment_three/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/segment_three/illustration.ly ... OK!
                Writing test_score/segments/segment_three/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/segments/segment_three/
        '''.replace('/', os.path.sep))
        assert not self.segments_path.joinpath(
            'segment_one',
            'illustration.pdf',
            ).exists()
        assert self.segments_path.joinpath(
            'segment_two',
            'illustration.pdf',
            ).exists()
        assert self.segments_path.joinpath(
            'segment_three',
            'illustration.pdf',
            ).exists()

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_one_segment(self, open_file_mock):
        self.create_score()
        self.create_segment('test_segment')
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
            Illustration candidates: 'test_segment' ...
                Reading test_score/segments/metadata.json ... OK!
            Illustrating test_score/segments/test_segment/
                Reading test_score/segments/metadata.json ... OK!
                Reading test_score/segments/test_segment/metadata.json ... JSON does not exist.
                Importing test_score.segments.test_segment.definition
                Writing test_score/segments/test_segment/metadata.json
                    Abjad runtime: ... second...
                Writing test_score/segments/test_segment/illustration.ly ... OK!
                Writing test_score/segments/test_segment/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/segments/test_segment/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.segments_path, self.expected_files)
        illustration_path = self.segments_path.joinpath(
            'test_segment', 'illustration.ly')
        self.compare_lilypond_contents(
            illustration_path,
            self.expected_illustration_contents,
            )
