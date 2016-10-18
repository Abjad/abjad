# -*- coding: utf-8 -*-
from __future__ import print_function
import doctest
import importlib
import os
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class DoctestScript(CommandlineScript):
    r'''Runs doctests on all Python files in current directory recursively.

    ..  shell::

        ajv doctest --help

    '''

    ### CLASS VARIABLES ###

    alias = 'doctest'
    short_description = 'Run doctests on all modules in current path.'

    _module_names_for_globs = (
        'abjad',
        'experimental',
        )

    ### PRIVATE METHODS ###

    def _get_file_paths(self, input_paths):
        ignored_directory_names = (
            '__pycache__',
            '.git',
            '.svn',
            'test',
            'docs',
            )
        file_paths = []
        for input_path in input_paths:
            if not os.path.exists(input_path):
                print('No such path {!r}'.format(input_path))
                sys.exit(1)
            elif os.path.isfile(input_path):
                file_paths.append(input_path)
            for current_root, directories, files in os.walk(input_path):
                for directory in directories[:]:
                    if directory in ignored_directory_names:
                        directories.remove(directory)
                    elif not os.path.exists(os.path.join(
                        current_root, directory, '__init__.py')):
                        directories.remove(directory)
                for file_name in files[:]:
                    if not file_name.endswith('.py'):
                        continue
                    file_path = os.path.join(current_root, file_name)
                    file_paths.append(file_path)
        return file_paths

    def _get_namespace(self):
        globs = {}
        for module_name in self._module_names_for_globs:
            try:
                module = importlib.import_module(module_name)
                globs.update(module.__dict__)
            except:
                pass
        try:
            ide_module = importlib.import_module('ide')
            globs['ide'] = ide_module
        except ImportError:
            pass
        globs['print_function'] = print_function
        config_parser = self._config_parser
        try:
            imports = config_parser.get(self.alias, 'imports')
        except:
            imports = ''
        imports = stringtools.normalize(imports).split('\n')
        for line in imports:
            exec(line, globs, globs)
        globs
        return globs

    def _get_optionflags(self, args):
        optionflags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS
            )
        if args and args.diff:
            optionflags = optionflags | doctest.REPORT_NDIFF
        if args and args.x:
            optionflags = optionflags | doctest.REPORT_ONLY_FIRST_FAILURE
        return optionflags

    def _process_args(
        self,
        args=None,
        file_paths=None,
        print_to_terminal=True,
        ):
        assert not (args and file_paths)
        result = []
        globs = self._get_namespace()
        optionflags = self._get_optionflags(args)
        total_failures = 0
        total_modules = 0
        total_tests = 0
        failed_file_paths = []
        error_messages = []
        file_paths = file_paths or self._get_file_paths(args.path)
        try:
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
                doctest_output = string_buffer.getvalue()
                if failure_count:
                    failed_file_paths.append(os.path.relpath(file_path))
                    error_messages.append(doctest_output)
                    if print_to_terminal:
                        result_code = ''.join((
                            self._colors['RED'],
                            'FAILED',
                            self._colors['END'],
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
                            self._colors['BLUE'],
                            'OK',
                            self._colors['END'],
                            ))
                        print(relative_path, result_code)
                    else:
                        result_code = 'OK'
                        string = '{} {}'.format(relative_path, result_code)
                        result.append(string)
                total_failures += failure_count
                total_tests += test_count
        except KeyboardInterrupt:
            print('Interrupted. Halting tests.')
        self._report(
            error_messages=error_messages,
            failed_file_paths=failed_file_paths,
            print_to_terminal=print_to_terminal,
            result=result,
            total_tests=total_tests,
            total_failures=total_failures,
            total_modules=total_modules,
            )

    def _report(
        self,
        error_messages=None,
        failed_file_paths=None,
        print_to_terminal=False,
        result=None,
        total_tests=None,
        total_failures=None,
        total_modules=None,
        ):
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
        if print_to_terminal:
            print()
        else:
            result.append('')
        test_identifier = stringtools.pluralize('test', total_tests)
        module_identifier = stringtools.pluralize('module', total_modules)
        string = (
            '{total_successes} passed, {total_failures} failed out of '
            '{total_tests} {test_identifier} '
            'in {total_modules} {module_identifier}.'
            )
        string = string.format(
            module_identifier=module_identifier,
            test_identifier=test_identifier,
            total_failures=total_failures,
            total_modules=total_modules,
            total_successes=total_tests - total_failures,
            total_tests=total_tests,
            )
        if print_to_terminal:
            print(string)
            if failed_file_paths:
                sys.exit(1)
            else:
                sys.exit(0)
        else:
            result.append(string)
            return result

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'path',
            default=[os.getcwd()],
            help='directory tree to be recursed over',
            nargs='*',
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
