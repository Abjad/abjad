import abjad
import doctest
import pathlib
import pytest
import re
import shutil
import sys
import unittest
import types
import uqbar.io
from io import StringIO


class ScorePackageScriptTestCase(unittest.TestCase):
    r'''A base test class for score-package scripts.
    '''

    ansi_escape = re.compile(r'\x1b[^m]*m')

    test_path = pathlib.Path(__file__).parent
    score_path = test_path.joinpath('test_score')
    build_path = score_path.joinpath('test_score', 'builds')
    distribution_path = score_path.joinpath('test_score', 'distribution')
    materials_path = score_path.joinpath('test_score', 'materials')
    segments_path = score_path.joinpath('test_score', 'segments')
    tools_path = score_path.joinpath('test_score', 'tools')

    # ### TEST LIFECYCLE ### #

    def setUp(self):
        if self.score_path.exists():
            shutil.rmtree(self.score_path)
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
                shutil.rmtree(path)
        sys.path.remove(str(self.score_path))
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith('test_score'):
                del(sys.modules[path])

    # ### UTILITY METHODS ### #

    def collect_segments(self):
        script = abjad.cli.ManageSegmentScript()
        command = ['--collect']
        with uqbar.io.DirectoryChange(self.score_path):
            script(command)

    def create_build_target(
        self,
        force=False,
        expect_error=False,
    ):
        script = abjad.cli.ManageBuildTargetScript()
        command = ['--new']
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.score_path):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
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
        script = abjad.cli.ManageMaterialScript()
        command = ['--new', material_name]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.score_path):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
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
        script = abjad.cli.ManageScoreScript()
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
        with uqbar.io.DirectoryChange(self.test_path):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
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
        script = abjad.cli.ManageSegmentScript()
        command = ['--new', segment_name]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.score_path):
            if expect_error:
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 1
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
        script = abjad.cli.ManageMaterialScript()
        command = ['--illustrate', material_name]
        with uqbar.io.DirectoryChange(self.score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segment(self, segment_name):
        script = abjad.cli.ManageSegmentScript()
        command = ['--illustrate', segment_name]
        with uqbar.io.DirectoryChange(self.score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segments(self):
        script = abjad.cli.ManageSegmentScript()
        command = ['--illustrate', '*']
        with uqbar.io.DirectoryChange(self.score_path):
            script(command)

    def install_fancy_segment_maker(self):
        segment_maker_path = self.tools_path.joinpath('SegmentMaker.py')
        with segment_maker_path.open('w') as file_pointer:
            file_pointer.write(pytest.helpers.get_fancy_segment_maker_code())
        parts_path = self.build_path.joinpath('parts.ily')
        with parts_path.open('w') as file_pointer:
            file_pointer.write(pytest.helpers.get_fancy_parts_code())

    # ### PUBLIC METHODS ### #

    def compare_captured_output(self, expected):
        actual = self.ansi_escape.sub('', self.string_io.getvalue())
        actual = abjad.String.normalize(actual)
        expected = abjad.String.normalize(expected)
        self.compare_strings(expected, actual)

    def compare_file_contents(self, path, expected_contents):
        expected_contents = abjad.String.normalize(expected_contents)
        with open(str(path), 'r') as file_pointer:
            contents = abjad.String.normalize(file_pointer.read())
        self.compare_strings(expected_contents, contents)

    def compare_lilypond_contents(self, ly_path, expected_contents):
        expected_contents = abjad.String.normalize(expected_contents)
        with open(str(ly_path), 'r') as file_pointer:
            contents = file_pointer.read()
        if ly_path.suffix == '.ly':
            contents = contents.splitlines()
            while 'version' not in contents[0]:
                contents.pop(0)
            contents.pop(0)
            contents = '\n'.join(contents)
        contents = abjad.String.normalize(contents)
        self.compare_strings(expected_contents, contents)

    def compare_path_contents(self, path_to_search, expected_files):
        actual_files = sorted(
            str(path.relative_to(self.test_path))
            for path in sorted(path_to_search.glob('**/*.*'))
            if '__pycache__' not in path.parts and
            path.suffix != '.pyc'
            )
        self.compare_strings(
            '\n'.join(str(_) for _ in actual_files),
            '\n'.join(str(_) for _ in expected_files),
            )

    def compare_strings(self, expected, actual):
        actual = self.normalize(self.ansi_escape.sub('', actual))
        expected = self.normalize(self.ansi_escape.sub('', expected))
        example = types.SimpleNamespace()
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

    def normalize(self, string):
        return abjad.String.normalize(string)

    def reset_string_io(self):
        self.string_io.close()
        self.string_io = StringIO()

    # ### PUBLIC PROPERTIES ### #

    @property
    def test_path(self):
        return pathlib.Path(__file__).parent
