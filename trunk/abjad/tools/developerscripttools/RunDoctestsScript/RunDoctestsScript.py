from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
import doctest
import importlib
import os


class RunDoctestsScript(DirectoryScript):
    '''Run doctests on all Python files in current directory recursively:

    ::

        bash$ ajv doctest -h
        usage: run-doctests [-h] [--version]

        Run doctests on all modules in current path.

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit

    Return `RunDoctestsScript` instance.
    '''

    ### PUBLIC READ-ONLY PROPERTIES ###

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
        globs = importlib.import_module('abjad').__dict__.copy()
        try:
            globs.update(importlib.import_module('experimental').__dict__)
        except ImportError:
            pass
        iotools.clear_terminal()
        total_modules = 0
        for dir_path, dir_names, file_names in os.walk('.'):
            for file_name in file_names:
                if file_name.endswith('.py') and \
                    not file_name.startswith('test_') and \
                    not file_name == '__init__.py':
                    total_modules += 1
                    full_file_name = os.path.abspath(os.path.join(dir_path, file_name))
                    doctest.testfile(full_file_name, module_relative = False, globs = globs,
                       optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
        print 'Total modules: %s' % total_modules

    def setup_argument_parser(self, parser):
        pass
