# -*- coding: utf-8 -*-
import argparse
import doctest
import re
import shutil
import sys
import unittest
from abjad.tools import commandlinetools
from abjad.tools import stringtools
from abjad.tools import systemtools
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ScorePackageScriptTestCase(unittest.TestCase):
    r'''A base test class for score-package scripts.
    '''

    ansi_escape = re.compile(r'\x1b[^m]*m')
    test_path = pathlib.Path(__file__).parent
    score_path = test_path.joinpath('test_score')
    build_path = score_path.joinpath('test_score', 'build')
    distribution_path = score_path.joinpath('test_score', 'distribution')
    materials_path = score_path.joinpath('test_score', 'materials')
    segments_path = score_path.joinpath('test_score', 'segments')
    tools_path = score_path.joinpath('test_score', 'tools')
    fancy_parts_code = stringtools.normalize(r"""
    \book {
        \bookOutputSuffix "cello"
        \score {
            \keepWithTag #'(time cello)
            \include "../segments.ily"
        }
    }
    \book {
        \bookOutputSuffix "viola"
        \score {
            \keepWithTag #'(viola)
            \include "../segments.ily"
        }
    }
    \book {
        \bookOutputSuffix "violin-i"
        \score {
            \keepWithTag #'(first-violin)
            \include "../segments.ily"
        }
    }
    \book {
        \bookOutputSuffix "violin-ii"
        \score {
            \keepWithTag #'(second-violin)
            \include "../segments.ily"
        }
    }
    """)
    fancy_segment_maker_code = stringtools.normalize(r"""
        # -*- coding: utf-8 -*-
        from abjad import attach
        from abjad import iterate
        from abjad import set_
        from abjad.tools import abctools
        from abjad.tools import indicatortools
        from abjad.tools import lilypondfiletools
        from abjad.tools import scoretools
        from abjad.tools import templatetools


        class SegmentMaker(abctools.AbjadObject):

            ### INITIALIZER ###

            def __init__(self, measure_count=1):
                measure_count = int(measure_count)
                assert 0 < measure_count
                self.measure_count = measure_count
                self.score_template = templatetools.StringQuartetScoreTemplate()

            ### SPECIAL METHODS ###

            def __call__(
                self,
                segment_metadata=None,
                previous_segment_metadata=None,
                ):
                score = self.score_template()
                for i in range(self.measure_count):
                    for voice in iterate(score).by_class(scoretools.Voice):
                        measure = scoretools.Measure((4, 4), "c'1")
                        voice.append(measure)
                lilypond_file = lilypondfiletools.make_basic_lilypond_file(
                    score,
                    includes=['../../stylesheets/stylesheet.ily'],
                    )
                first_bar_number = segment_metadata.get('first_bar_number', 1)
                if 1 < first_bar_number:
                    set_(score).current_bar_number = first_bar_number
                segment_number = segment_metadata.get('segment_number', 1)
                segment_count = segment_metadata.get('segment_count', 1)
                if 1 < segment_number:
                    rehearsal_mark = indicatortools.RehearsalMark()
                    for voice in iterate(score).by_class(scoretools.Voice):
                        for leaf in iterate(voice).by_class(scoretools.Leaf):
                            attach(rehearsal_mark, leaf)
                            break
                if segment_count <= segment_number:
                    score.add_final_bar_line(
                        abbreviation='|.',
                        to_each_voice=True,
                        )
                segment_metadata['measure_count'] = self.measure_count
                return lilypond_file, segment_metadata
    """)

    ### TEST LIFECYCLE ###

    def setUp(self):
        if self.score_path.exists():
            shutil.rmtree(str(self.score_path))
        self.directory_items = set(self.test_path.iterdir())
        sys.path.insert(0, str(self.score_path))
        self.string_io = StringIO()

    def tearDown(self):
        self.string_io.close()
        for path in sorted(self.test_path.iterdir()):
            if path in self.directory_items:
                continue
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(str(path))
        sys.path.remove(str(self.score_path))
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith('test_score'):
                del(sys.modules[path])

    ### UTILITY METHODS ###

    def collect_segments(self):
        script = commandlinetools.ManageSegmentScript()
        command = ['--collect']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            script(command)

    def compare_captured_output(self, expected):
        actual = self.ansi_escape.sub('', self.string_io.getvalue())
        actual = stringtools.normalize(actual)
        expected = stringtools.normalize(expected)
        self.compare_strings(expected, actual)

    def compare_file_contents(self, path, expected_contents):
        expected_contents = stringtools.normalize(expected_contents)
        with open(str(path), 'r') as file_pointer:
            contents = stringtools.normalize(file_pointer.read())
        self.compare_strings(expected_contents, contents)

    def compare_lilypond_contents(self, ly_path, expected_contents):
        expected_contents = stringtools.normalize(expected_contents)
        with open(str(ly_path), 'r') as file_pointer:
            contents = file_pointer.read()
        if ly_path.suffix == '.ly':
            contents = contents.splitlines()
            while 'version' not in contents[0]:
                contents.pop(0)
            contents.pop(0)
            contents = '\n'.join(contents)
        contents = stringtools.normalize(contents)
        self.compare_strings(expected_contents, contents)

    def compare_path_contents(self, path_to_search, expected_files):
        actual_files = sorted(
            str(path.relative_to(self.test_path))
            for path in path_to_search.glob('**/*.*')
            if '__pycache__' not in path.parts and
            path.suffix != '.pyc'
            )
        assert actual_files == expected_files

    def compare_strings(self, expected, actual):
        example = argparse.Namespace()
        example.want = expected
        output_checker = doctest.OutputChecker()
        flags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS |
            doctest.REPORT_NDIFF
            )
        success = output_checker.check_output(expected, actual, flags)
        if not success:
            diff = output_checker.output_difference(example, actual, flags)
            raise Exception(diff)

    def create_build_target(
        self,
        force=False,
        expect_error=False,
        ):
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--new']
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.build_path.joinpath('letter-portrait')

    def create_material(
        self,
        material_name='test_material',
        force=False,
        expect_error=False,
        ):
        script = commandlinetools.ManageMaterialScript()
        command = ['--new', material_name]
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.score_path.joinpath(
            self.score_path.name,
            'materials',
            material_name,
            )

    def create_score(self, force=False, expect_error=False):
        script = commandlinetools.ManageScoreScript()
        command = [
            '--new',
            'Test Score',
            '-y', '2016',
            '-n', 'Josiah Wolf Oberholtzer',
            '-e', 'josiah.oberholtzer@gmail.com',
            '-g', 'josiah-wolf-oberholtzer',
            '-l', 'consort',
            '-w', 'www.josiahwolfoberholtzer.com',
            ]
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')

    def create_segment(
        self,
        segment_name='test_segment',
        force=False,
        expect_error=False,
        ):
        script = commandlinetools.ManageSegmentScript()
        command = ['--new', segment_name]
        if force:
            command.insert(0, '-f')
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.score_path.joinpath(
            self.score_path.name,
            'segments',
            segment_name,
            )

    def illustrate_material(self, material_name):
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', material_name]
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segment(self, segment_name):
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', segment_name]
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segments(self):
        script = commandlinetools.ManageSegmentScript()
        command = ['--illustrate', '*']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            script(command)

    def install_fancy_segment_maker(self):
        segment_maker_path = self.tools_path.joinpath('SegmentMaker.py')
        with open(str(segment_maker_path), 'w') as file_pointer:
            file_pointer.write(self.fancy_segment_maker_code)
        parts_path = self.build_path.joinpath('parts.ily')
        with open(str(parts_path), 'w') as file_pointer:
            file_pointer.write(self.fancy_parts_code)

    def reset_string_io(self):
        self.string_io.close()
        self.string_io = StringIO()
