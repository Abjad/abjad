import abjad
import pathlib
import pytest
import re
import shutil
import sys
import unittest
import uqbar.io
import uqbar.strings


class ScorePackageScriptTestCase(unittest.TestCase):
    r'''A base test class for score-package scripts.
    '''

    ansi_escape = re.compile(r'\x1b[^m]*m')

    test_directory_path = pathlib.Path(__file__).parent
    score_path = test_directory_path.joinpath('test_score')
    build_path = score_path.joinpath('test_score', 'builds')
    distribution_path = score_path.joinpath('test_score', 'distribution')
    materials_path = score_path.joinpath('test_score', 'materials')
    segments_path = score_path.joinpath('test_score', 'segments')
    tools_path = score_path.joinpath('test_score', 'tools')

    # ### TEST LIFECYCLE ### #

    def setUp(self):
        if self.score_path.exists():
            shutil.rmtree(self.score_path)
        self.directory_items = set(self.test_directory_path.iterdir())
        sys.path.insert(0, str(self.score_path))

    def tearDown(self):
        for path in sorted(self.test_directory_path.iterdir()):
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

    def collect_segments(test_directory_path):
        script = abjad.cli.ManageSegmentScript()
        command = ['--collect']
        score_path = test_directory_path / package_name
        with uqbar.io.DirectoryChange(score_path):
            script(command)

    def illustrate_material(test_directory_path, material_name):
        script = abjad.cli.ManageMaterialScript()
        command = ['--illustrate', material_name]
        score_path = test_directory_path / package_name
        with uqbar.io.DirectoryChange(score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segment(test_directory_path, segment_name):
        script = abjad.cli.ManageSegmentScript()
        command = ['--illustrate', segment_name]
        score_path = test_directory_path / package_name
        with uqbar.io.DirectoryChange(score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segments(test_directory_path):
        script = abjad.cli.ManageSegmentScript()
        command = ['--illustrate', '*']
        score_path = test_directory_path / package_name
        with uqbar.io.DirectoryChange(score_path):
            script(command)

    def install_fancy_segment_maker(self):
        segment_maker_path = self.tools_path.joinpath('SegmentMaker.py')
        with segment_maker_path.open('w') as file_pointer:
            file_pointer.write(pytest.helpers.get_fancy_segment_maker_code())
        parts_path = self.build_path.joinpath('parts.ily')
        with parts_path.open('w') as file_pointer:
            file_pointer.write(pytest.helpers.get_fancy_parts_code())

    # ### PUBLIC METHODS ### #

    def compare_captured_output(self, actual, expected):
        actual = self.ansi_escape.sub('', actual)
        actual = uqbar.strings.normalize(actual)
        expected = uqbar.strings.normalize(expected)
        pytest.helpers.compare_strings(
            expected=expected,
            actual=actual,
        )

    def compare_file_contents(self, path, expected_contents):
        expected_contents = uqbar.strings.normalize(expected_contents)
        with open(str(path), 'r') as file_pointer:
            contents = uqbar.strings.normalize(file_pointer.read())
        pytest.helpers.compare_strings(
            actual=contents,
            expected=expected_contents,
        )

    def compare_lilypond_contents(self, ly_path, expected_contents):
        expected_contents = uqbar.strings.normalize(expected_contents)
        with open(str(ly_path), 'r') as file_pointer:
            contents = file_pointer.read()
        if ly_path.suffix == '.ly':
            contents = contents.splitlines()
            while 'version' not in contents[0]:
                contents.pop(0)
            contents.pop(0)
            contents = '\n'.join(contents)
        contents = uqbar.strings.normalize(contents)
        pytest.helpers.compare_strings(
            expected=expected_contents,
            actual=contents,
        )
