# -*- coding: utf-8 -*-
import argparse
import doctest
import re
import unittest
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestCase(unittest.TestCase):

    ### CLASS VARIABLES ###

    ansi_escape = re.compile(r'\x1b[^m]*m')

    ### PUBLIC METHODS ###

    def compare_captured_output(self, expected):
        from abjad.tools import stringtools
        actual = self.ansi_escape.sub('', self.string_io.getvalue())
        actual = stringtools.normalize(actual)
        expected = stringtools.normalize(expected)
        self.compare_strings(expected, actual)

    def compare_file_contents(self, path, expected_contents):
        from abjad.tools import stringtools
        expected_contents = stringtools.normalize(expected_contents)
        with open(str(path), 'r') as file_pointer:
            contents = stringtools.normalize(file_pointer.read())
        self.compare_strings(expected_contents, contents)

    def compare_lilypond_contents(self, ly_path, expected_contents):
        from abjad.tools import stringtools
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
        actual = self.normalize(self.ansi_escape.sub('', actual))
        expected = self.normalize(self.ansi_escape.sub('', expected))
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

    def normalize(self, string):
        from abjad.tools import stringtools
        return stringtools.normalize(string)

    def reset_string_io(self):
        self.string_io.close()
        self.string_io = StringIO()

    def setUp(self):
        self.string_io = StringIO()

    def tearDown(self):
        self.string_io.close()

    ### PUBLIC PROPERTIES ###

    @property
    def test_path(self):
        return pathlib.Path(__file__).parent
