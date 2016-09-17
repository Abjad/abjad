# -*- encoding: utf-8 -*-
import argparse
import doctest
import os
import re
import shutil
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


class TestCase(unittest.TestCase):

    ansi_escape = re.compile(r'\x1b[^m]*m')
    test_path = pathlib.Path(__file__).parent
    temp_test_dir_name = 'temp_test_dir'
    subdirectory_path = test_path.joinpath(temp_test_dir_name)

    # Specific test case file contents
    test_bad_header_order_module_path = subdirectory_path.joinpath(
        'BadHeaderOrder.py'
        )
    test_property_in_methods_module_path = subdirectory_path.joinpath(
        'PropInMethods.py'
        )
    test_method_in_properties_module_path = subdirectory_path.joinpath(
        'MethodInProps.py'
        )
    test_passing_module_path = subdirectory_path.joinpath(
        'GoodClass.py'
        )
    test_bad_header_order_module_contents = stringtools.normalize(r'''
    class BadHeaderClass:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        def __init__(self):
            pass
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        ### PUBLIC PROPERTIES ###
        ### PRIVATE PROPERTIES ###
        # ^ Properties are out of order
    ''')
    test_property_in_methods_module_contents = stringtools.normalize(r'''
    class PropertyInMethods:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        def __init__(self):
            pass
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        @property
        def i_dont_belong_here(self):
            pass
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
    ''')
    test_method_in_properties_module_contents = stringtools.normalize(r'''
    class MethodInProperties:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        def __init__(self):
            pass
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
        def i_dont_belong_here(self):
            pass
    ''')
    test_passing_module_contents = stringtools.normalize(r'''
    class PassingClass:
        ### CLASS VARIABLES ###
        x = 5
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        def __init__(self):
            pass
        ### SPECIAL METHODS ###
        def __str__(self):
            print("Hello, testing!")
        ### PRIVATE METHODS ###
        def _some_private_method(self):
            pass
        ### PUBLIC METHODS ###
        def some_public_method(self):
            pass
        ### PRIVATE PROPERTIES ###
        @property
        def _i_belong_here(self):
            pass
        @_i_belong_here.setter
        def _i_belong_here(self, value):
            pass
        ### PUBLIC PROPERTIES ###
        @property
        def i_belong_here(self):
            pass
        @i_belong_here.setter
        def i_belong_here(self, value):
            pass
    ''')
    test_cases = [
        (test_bad_header_order_module_path,
         test_bad_header_order_module_contents),
        (test_method_in_properties_module_path,
         test_method_in_properties_module_contents),
        (test_property_in_methods_module_path,
         test_property_in_methods_module_contents),
        (test_passing_module_path,
         test_passing_module_contents)
        ]

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

    def setUp(self):
        if not self.subdirectory_path.exists():
            self.subdirectory_path.mkdir()
        for case in self.test_cases:
            with open(str(case[0]), 'w') as file_pointer:
                file_pointer.write(case[1])
        self.string_io = StringIO()

    def tearDown(self):
        shutil.rmtree(str(self.subdirectory_path))
        self.string_io.close()

    def test_check_class_sections(self):
        script = commandlinetools.CheckClassSections()
        command = [str(self.subdirectory_path)]
        with systemtools.TemporaryDirectoryChange(str(self.test_path)):
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
        assert context_manager.exception.code == 1
        script_output = self.ansi_escape.sub('', self.string_io.getvalue())
        script_output = stringtools.normalize(script_output)
        expected = stringtools.normalize('''
Recursively scanning {} for errors...
Errors in {}:
Lines [10]: BAD HEADER ORDER
===============================================================================
Errors in {}:
Lines [11]: METHOD IN PROPERTIES SECTION
===============================================================================
Errors in {}:
Lines [9]: PROPERTY IN METHODS SECTION
===============================================================================
4 total files checked.
1 passed.
3 failed.
        '''.format(
                self.temp_test_dir_name,
                self.test_bad_header_order_module_path,
                self.test_method_in_properties_module_path,
                self.test_property_in_methods_module_path,
            )
        )
        self.compare_strings(expected, script_output)
