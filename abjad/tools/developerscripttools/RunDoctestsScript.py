# -*- encoding: utf-8 -*-
from __future__ import print_function
import doctest
import importlib
import os
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class RunDoctestsScript(DirectoryScript):
    r'''Runs doctests on all Python files in current directory recursively.

    ..  shell::

        ajv doctest --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'doctest'``.
        '''
        return 'doctest'

    @property
    def long_description(self):
        r'''Long description of  script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns none.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Run doctests on all modules in current path.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PUBLIC PROPERTIES ###

    def process_args(
        self,
        args=None,
        file_paths=None,
        print_to_terminal=True,
        ):
        r'''Processes `args`.

        Returns none when `print_to_terminal` is false.

        Returns string(s) when `print_to_terminal` is true.

        Returns none.
        '''
        assert not (args and file_paths)
        result = []
        globs = importlib.import_module('abjad').__dict__.copy()
        try:
            experimental_module = importlib.import_module('experimental')
            experimental_demos_module = importlib.import_module('experimental')
            globs.update(experimental_module.__dict__)
            globs.update(experimental_demos_module.__dict__)
        except:
            pass
        try:
            ide_module = importlib.import_module('ide')
            globs['ide'] = ide_module
        except:
            pass
        globs['print_function'] = print_function
        optionflags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS
            )
        if args and args.diff:
            optionflags = optionflags | doctest.REPORT_NDIFF
        if args and args.x:
            optionflags = optionflags | doctest.REPORT_ONLY_FIRST_FAILURE
        total_failures = 0
        total_modules = 0
        total_tests = 0
        failed_file_paths = []
        error_messages = []
        if not file_paths:
            file_paths = []
            if os.path.isdir(args.path):
                for dir_path, dir_names, file_names in os.walk(args.path):
                    dir_names[:] = [x for x in dir_names
                        if not x.startswith(('.', 'mothballed'))]
                    for file_name in sorted(file_names):
                        if (file_name.endswith('.py') and
                            not file_name.startswith('test_') and
                            not file_name == '__init__.py'):
                            file_path = os.path.abspath(
                                os.path.join(dir_path, file_name))
                            file_paths.append(file_path)
            elif os.path.isfile(args.path):
                file_paths.append(args.path)
        for file_path in sorted(file_paths):
            total_modules += 1
            relative_path = os.path.relpath(file_path)
            string_buffer = StringIO()
            with systemtools.RedirectedStreams(stdout=string_buffer):
                failure_count, test_count = doctest.testfile(
                    file_path,
                    module_relative=False,
                    globs=globs,
                    optionflags=optionflags,
                    )
            if failure_count:
                failed_file_paths.append(os.path.relpath(file_path))
                error_messages.append(string_buffer.getvalue())
                if print_to_terminal:
                    result_code = ''.join((
                        self.colors['RED'],
                        'FAILED',
                        self.colors['END'],
                        ))
                    print(relative_path, result_code)
                else:
                    result_code = 'FAILED'
                    string = '{} {}'.format(relative_path, result_code)
                    result.append(string)
                if args and args.x:
                    break
            else:
                if print_to_terminal:
                    result_code = ''.join((
                        self.colors['BLUE'],
                        'OK',
                        self.colors['END'],
                        ))
                    print(relative_path, result_code)
                else:
                    result_code = 'OK'
                    string = '{} {}'.format(relative_path, result_code)
                    result.append(string)
            total_failures += failure_count
            total_tests += test_count
        if failed_file_paths:
            if print_to_terminal:
                print()
            else:
                result.append('')
            for error_message in error_messages:
                if print_to_terminal:
                    print(error_message)
                else:
                    result.append(error_message)
        for file_path in failed_file_paths:
            string = 'FAILED: {}'.format(file_path)
            if print_to_terminal:
                print(string)
            else:
                result.append(string)
        total_successes = total_tests - total_failures
        if print_to_terminal:
            print()
        else:
            result.append('')
        test_identifier = stringtools.pluralize('test', total_tests)
        module_identifier = stringtools.pluralize('module', total_modules)
        string = '{} of {} {} passed in {} {}.'
        string = string.format(
            total_successes,
            total_tests,
            test_identifier,
            total_modules,
            module_identifier,
            )
        if print_to_terminal:
            print(string)
            if total_successes == total_tests:
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            result.append(string)
            return result


    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            )
        parser.add_argument(
            '--diff',
            action='store_true',
            help='print diff-like output on failed tests.',
            )
        parser.add_argument(
            '-x',
            action='store_true',
            help='stop after first failure.',
            )