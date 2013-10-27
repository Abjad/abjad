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
        if args.diff:
            optionflags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS|doctest.REPORT_NDIFF
        else:
            optionflags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
        iotools.clear_terminal()
        total_modules = 0
        for dir_path, dir_names, file_names in os.walk('.'):
            for file_name in file_names:
                if file_name.endswith('.py') and \
                    not file_name.startswith('test_') and \
                    not file_name == '__init__.py':
                    total_modules += 1
                    full_file_name = os.path.abspath(
                        os.path.join(dir_path, file_name))
                    doctest.testfile(
                        full_file_name, 
                        module_relative=False, 
                        globs=globs,
                       optionflags=optionflags,
                       )
        print 'Total modules: %s' % total_modules

    def setup_argument_parser(self, parser):
        parser.add_argument('--diff',
            action='store_true',
            help='print diff-like output on failed tests.',
            )
