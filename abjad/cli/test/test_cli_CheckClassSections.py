import abjad
import pathlib
import pytest
import re
import shutil
import unittest
import uqbar.io
from io import StringIO
from uqbar.strings import normalize


class TestCheckClassSections(unittest.TestCase):

    ansi_escape = re.compile(r'\x1b[^m]*m')
    test_directory_path = pathlib.Path(__file__).parent
    temp_test_dir_name = 'temp_test_dir'
    subdirectory = test_directory_path.joinpath(temp_test_dir_name)

    # Specific test case file contents
    test_bad_header_order_module_path = subdirectory.joinpath(
        'BadHeaderOrder.py'
    )
    test_property_in_methods_module_path = subdirectory.joinpath(
        'PropInMethods.py'
    )
    test_method_in_properties_module_path = subdirectory.joinpath(
        'MethodInProps.py'
    )
    test_multiple_errors_in_file_module_path = subdirectory.joinpath(
        'MultipleErrors.py'
    )
    test_multiple_classes_in_one_module_path = subdirectory.joinpath(
        'MultipleClasses.py'
    )
    test_passing_module_path = subdirectory.joinpath(
        'GoodClass.py'
    )
    test_non_property_decorators_module_path = subdirectory.joinpath(
        'NonPropertyDecorators.py'
    )
    test_bad_header_order_module_contents = normalize(r'''
    class BadHeaders:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        ### PUBLIC PROPERTIES ###
        ### PRIVATE PROPERTIES ###
        # ^ Properties are out of order
    ''')
    test_property_in_methods_module_contents = normalize(r'''
    class PropertyInMethods:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        @property
        def i_dont_belong_here(self):
            pass
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
    ''')
    test_method_in_properties_module_contents = normalize(r'''
    class MethodInProperties:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
        def i_dont_belong_here(self):
            pass
    ''')
    test_multiple_errors_in_file_module_contents = normalize(r'''
    class MultipleErrors:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        @property
        def doesnt_belong_here(self):
            pass
        @property
        def also_doesnt_belong_here(self):
            pass
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
        def i_dont_belong_here(self):
            pass
    ''')
    test_multiple_classes_in_one_module_contents = normalize(r'''
    class GoodClassOne:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
        pass
    class GoodClassTwo:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
        pass
    ''')
    test_non_property_decorators_module_contents = normalize(r'''
    class NonPropertyDecoratorsInMethods:
        ### CLASS VARIABLES ###
        ### CONSTRUCTOR ###
        ### INITIALIZER ###
        ### SPECIAL METHODS ###
        ### PRIVATE METHODS ###
        ### PUBLIC METHODS ###
        @staticmethod
        def i_belong_here(self):
            pass
        @classmethod
        def me_too(self):
            pass
        @abc.abstractmethod
        def me_three(self):
            pass
        @lex.TOKEN()
        def me_four(self):
            pass
        ### PRIVATE PROPERTIES ###
        ### PUBLIC PROPERTIES ###
    ''')
    test_passing_module_contents = normalize(r'''
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

    # ### TEST HELPER METHODS ### #

    def tearDown(self):
        shutil.rmtree(str(self.subdirectory))

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
        if none is passed, `self.test_directory_path` is used.

        This method actually touches the file system, creating a temporary
        directory at `self.temp_test_dir_name` and creating temporary
        modules as specified in `modules`. `self.tearDown()` cleans up after
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
            test_working_directory = self.test_directory_path
        # Create temporary testing modules
        if not self.subdirectory.exists():
            self.subdirectory.mkdir()
        for case in modules:
            with open(str(case[0]), 'w') as file_pointer:
                file_pointer.write(case[1])
        string_io = StringIO()
        # cd into test_working_directory and run the script with commands
        with uqbar.io.DirectoryChange(str(test_working_directory)):
            with uqbar.io.RedirectedStreams(stdout=string_io):
                with pytest.raises(SystemExit) as exception_info:
                    script = abjad.cli.CheckClassSections()
                    script(command)
        # Normalize script output for sane diffs
        script_output = self.ansi_escape.sub('', string_io.getvalue())
        script_output = normalize(script_output)
        return (script_output, exception_info.value.code)

    # ### TEST CASES ### #

    def test_bad_header_order(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            Errors in {}:
            Lines [8]: BAD HEADER ORDER
            ===============================================================================
            1 total files checked.
            0 passed.
            1 failed.
        ''').format(
            self.temp_test_dir_name,
            self.test_bad_header_order_module_path,
        )
        test_modules = [
            (self.test_bad_header_order_module_path,
             self.test_bad_header_order_module_contents),
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 1

    def test_method_in_properties(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            Errors in {}:
            Lines [9]: METHOD IN PROPERTIES SECTION
            ===============================================================================
            1 total files checked.
            0 passed.
            1 failed.
        ''').format(
            self.temp_test_dir_name,
            self.test_method_in_properties_module_path,
        )
        test_modules = [
            (self.test_method_in_properties_module_path,
             self.test_method_in_properties_module_contents),
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 1

    def test_property_in_methods(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            Errors in {}:
            Lines [7]: PROPERTY IN METHODS SECTION
            ===============================================================================
            1 total files checked.
            0 passed.
            1 failed.
        ''').format(
            self.temp_test_dir_name,
            self.test_property_in_methods_module_path,
        )
        test_modules = [
            (self.test_property_in_methods_module_path,
             self.test_property_in_methods_module_contents),
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 1

    def test_multiple_errors_in_file(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            Errors in {}:
            Lines [15]: METHOD IN PROPERTIES SECTION
            Lines [7, 10]: PROPERTY IN METHODS SECTION
            ===============================================================================
            1 total files checked.
            0 passed.
            1 failed.
        ''').format(
            self.temp_test_dir_name,
            self.test_multiple_errors_in_file_module_path,
        )
        test_modules = [
            (self.test_multiple_errors_in_file_module_path,
             self.test_multiple_errors_in_file_module_contents),
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 1

    def test_non_property_decorators_in_methods_passes(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            1 total files checked.
            1 passed.
            0 failed.
            '''.format(self.temp_test_dir_name)
        )
        test_modules = [
            (self.test_non_property_decorators_module_path,
             self.test_non_property_decorators_module_contents),
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 0

    def test_multiple_classes_in_one_module(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            1 total files checked.
            1 passed.
            0 failed.
        ''').format(self.temp_test_dir_name)
        test_modules = [
            (self.test_multiple_classes_in_one_module_path,
             self.test_multiple_classes_in_one_module_contents)
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 0

    def test_passing_case(self):
        expected = normalize('''
            Recursively scanning {} for errors...
            1 total files checked.
            1 passed.
            0 failed.
        ''').format(self.temp_test_dir_name)
        test_modules = [
            (self.test_passing_module_path,
             self.test_passing_module_contents)
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules, self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 0

    def test_passing_case_without_passing_path(self):
        expected = normalize('''
            Recursively scanning current working directory for errors...
            1 total files checked.
            1 passed.
            0 failed.
        ''').format(self.temp_test_dir_name)
        test_modules = [
            (self.test_passing_module_path,
             self.test_passing_module_contents)
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules,
            working_directory=self.subdirectory
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 0

    def test_passing_file_instead_of_dir(self):
        expected = normalize('''
            Scanning {} for errors...
            1 total files checked.
            1 passed.
            0 failed.
        ''').format(self.test_passing_module_path)
        test_modules = [
            (self.test_passing_module_path,
             self.test_passing_module_contents)
        ]
        # Run test
        script_output, exit_code = self.run_script_on_modules(
            test_modules,
            script_args=self.test_passing_module_path
        )
        pytest.helpers.compare_strings(expected=expected, actual=script_output)
        assert exit_code == 0
