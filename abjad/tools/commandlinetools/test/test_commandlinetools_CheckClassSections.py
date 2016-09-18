# -*- encoding: utf-8 -*-
import argparse
import doctest
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

    ### TEST HELPER METHODS ###
    
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

    def create_test_modules(self, modules):
        r'''Create temporary test case modules.
        
        `modules` should be a list of 2-tuples of strings in the form of
        (file_name, file_contents).

        This writes files within the directory `self.subdirectory_path`,
        and should be cleaned up after by `self.tearDown()`.
        '''
        if not self.subdirectory_path.exists():
            self.subdirectory_path.mkdir()
        for case in modules:
            with open(str(case[0]), 'w') as file_pointer:
                file_pointer.write(case[1])
        self.string_io = StringIO()

    def tearDown(self):
        shutil.rmtree(str(self.subdirectory_path))
        self.string_io.close()

    def run_script_on_modules(
        self,
        modules,
        script_args=None,
        working_directory=None
        ):
        r'''Return the output and exit code of CheckClassSections
        when run against `modules`.
        
        `modules` should be a list of 2-tuples of strings in the form of
        (file_name, file_contents).
        
        `script_args` is an optional list of arguments to be passed to
        CheckClassSections.

        `working_directory` is an optional directory to run the script from.
        if none is passed, `self.test_path` is used.
        
        This method actually touches the file system, creating a temporary
        directory at `self.temp_test_dir_name` and creating temporary
        modules as specified in `modules`. `self.tearDown` cleans up after
        this method.

        Returns a 2-tuple of (script_output, exit_code).
        '''
        # Handle arguments
        if script_args:
            if isinstance(script_args, list):
                command = [s_arg for s_arg in map(str, script_args)]
            else:
                command = [str(script_args)]
        else:
            command = []
        if working_directory:
            test_working_directory = working_directory
        else:
            test_working_directory = self.test_path
        # Create temporary testing modules
        if not self.subdirectory_path.exists():
            self.subdirectory_path.mkdir()
        for case in modules:
            with open(str(case[0]), 'w') as file_pointer:
                file_pointer.write(case[1])
        self.string_io = StringIO()
        # cd into test_working_directory and run the script with commands
        with systemtools.TemporaryDirectoryChange(str(test_working_directory)):
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script = commandlinetools.CheckClassSections()
                    script(command)
        # Normalize script output for sane diffs
        script_output = self.ansi_escape.sub('', self.string_io.getvalue())
        script_output = stringtools.normalize(script_output)
        return (script_output, context_manager.exception.code)

    ### TEST CASES ###
    
    def test_bad_header_order(self):
        expected = stringtools.normalize('''
Recursively scanning {} for errors...
Errors in {}:
Lines [10]: BAD HEADER ORDER
===============================================================================
1 total files checked.
0 passed.
1 failed.
        '''.format(
                self.temp_test_dir_name,
                self.test_bad_header_order_module_path,
             )
        )
        test_modules = [
            (self.test_bad_header_order_module_path,
             self.test_bad_header_order_module_contents),
             ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory_path
            )
        self.compare_strings(expected, script_output)
        self.assertEqual(exit_code, 1)

    def test_method_in_properties(self):
        expected = stringtools.normalize('''
Recursively scanning {} for errors...
Errors in {}:
Lines [11]: METHOD IN PROPERTIES SECTION
===============================================================================
1 total files checked.
0 passed.
1 failed.
        '''.format(
                self.temp_test_dir_name,
                self.test_method_in_properties_module_path,
             )
        )
        test_modules = [
            (self.test_method_in_properties_module_path,
             self.test_method_in_properties_module_contents),
            ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory_path
            )
        self.compare_strings(expected, script_output)
        self.assertEqual(exit_code, 1)

    def test_property_in_methods(self):
        expected = stringtools.normalize('''
Recursively scanning {} for errors...
Errors in {}:
Lines [9]: PROPERTY IN METHODS SECTION
===============================================================================
1 total files checked.
0 passed.
1 failed.
        '''.format(
                self.temp_test_dir_name,
                self.test_property_in_methods_module_path,
            )
        )
        test_modules = [
            (self.test_property_in_methods_module_path,
             self.test_property_in_methods_module_contents),
             ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory_path
            )
        self.compare_strings(expected, script_output)
        self.assertEqual(exit_code, 1)

    def test_passing_case(self):
        expected = stringtools.normalize('''
Recursively scanning {} for errors...
1 total files checked.
1 passed.
0 failed.
        '''.format(self.temp_test_dir_name)
        )
        test_modules = [
            (self.test_passing_module_path,
             self.test_passing_module_contents)
            ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory_path
            )
        self.compare_strings(expected, script_output)
        self.assertEqual(exit_code, 0)

    def test_passing_case_without_passing_path(self):
        expected = stringtools.normalize('''
Recursively scanning current working directory for errors...
1 total files checked.
1 passed.
0 failed.
        '''.format(self.temp_test_dir_name)
        )
        test_modules = [
            (self.test_passing_module_path,
             self.test_passing_module_contents)
            ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules,
            working_directory=self.temp_test_dir_name
            )
        self.compare_strings(expected, script_output)
        self.assertEqual(exit_code, 0)

