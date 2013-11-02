# -*- encoding: utf-8 -*-
import importlib
import os
from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class RunDoctestsScript(DirectoryScript):
    r'''Run doctests on all Python files in current directory recursively:

    ..  shell::

        ajv doctest --help

    Return `RunDoctestsScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'doctest'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'Run doctests on all modules in current path.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC PROPERTIES ###

    def process_args(self, args):
        import doctest
        globs = importlib.import_module('abjad').__dict__.copy()
        try:
            globs.update(importlib.import_module('experimental').__dict__)
            globs.update(
                importlib.import_module('experimental.demos').__dict__)
        except:
            pass
        optionflags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS
            )
        if args.diff:
            optionflags = optionflags | doctest.REPORT_NDIFF
        iotools.clear_terminal()
        total_failures = 0
        total_modules = 0
        total_tests = 0
        failed_file_paths = []
        for dir_path, dir_names, file_names in os.walk('.'):
            for file_name in file_names:
                if file_name.endswith('.py') and \
                    not file_name.startswith('test_') and \
                    not file_name == '__init__.py':
                    total_modules += 1
                    file_path = os.path.abspath(
                        os.path.join(dir_path, file_name))
                    print os.path.relpath(file_path)
                    failure_count, test_count = doctest.testfile(
                        file_path,
                        module_relative=False,
                        globs=globs,
                        optionflags=optionflags,
                        )
                    if failure_count:
                        failed_file_paths.append(os.path.relpath(file_path))
                    total_failures += failure_count
                    total_tests += test_count
        if failed_file_paths:
            print
        for file_path in failed_file_paths:
            print 'FAILED: {}'.format(file_path)
        total_successes = total_tests - total_failures
        print
        print '{} of {} tests passed in {} modules.'.format(
            total_successes,
            total_tests,
            total_modules,
            )

    def setup_argument_parser(self, parser):
        parser.add_argument('--diff',
            action='store_true',
            help='print diff-like output on failed tests.',
            )
