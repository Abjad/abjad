# -*- encoding: utf-8 -*-
import importlib
import os
import StringIO
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


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

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        import doctest
        globs = importlib.import_module('abjad').__dict__.copy()
        try:
            experimental_module = importlib.import_module('experimental')
            experimental_demos_module = importlib.import_module('experimental')
            globs.update(experimental_module.__dict__)
            globs.update(experimental_demos_module.__dict__)
        except:
            pass
        try:
            scoremanager_module = importlib.import_module('scoremanager')
            globs['scoremanager'] = scoremanager_module
        except:
            pass
        optionflags = (
            doctest.NORMALIZE_WHITESPACE |
            doctest.ELLIPSIS
            )
        if args.diff:
            optionflags = optionflags | doctest.REPORT_NDIFF
        #systemtools.IOManager.clear_terminal()
        total_failures = 0
        total_modules = 0
        total_tests = 0
        failed_file_paths = []
        error_messages = []
        for dir_path, dir_names, file_names in os.walk(args.path):
            for file_name in sorted(file_names):
                if file_name.endswith('.py') and \
                    not file_name.startswith('test_') and \
                    not file_name == '__init__.py':
                    total_modules += 1
                    file_path = os.path.abspath(
                        os.path.join(dir_path, file_name))
                    print os.path.relpath(file_path),
                    string_buffer = StringIO.StringIO()
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
                        print ''.join((
                            self.colors['RED'],
                            'FAILED',
                            self.colors['END'],
                            ))
                    else:
                        print ''.join((
                            self.colors['BLUE'],
                            'OK',
                            self.colors['END'],
                            ))
                    total_failures += failure_count
                    total_tests += test_count
        if failed_file_paths:
            print
            for error_message in error_messages:
                print error_message
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
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument('path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            )
        parser.add_argument('--diff',
            action='store_true',
            help='print diff-like output on failed tests.',
            )
