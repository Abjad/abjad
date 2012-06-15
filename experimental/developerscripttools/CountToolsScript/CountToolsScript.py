from abjad.tools import documentationtools
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import argparse
import importlib
import os


class CountToolsScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'tools'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'count'

    @property
    def short_description(self):
        return 'Count tools in PATH.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _is_valid_path(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
        return False

    def _validate_path(self, path):
        error = argparse.ArgumentTypeError('{!r} is not a valid directory.'.format(path))
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return path

    ### PUBLIC METHODS ###

    def process_args(self, args):
        print args

        private_classes = []
        private_functions = []
        public_classes = []
        public_functions = []

        for module in documentationtools.ModuleCrawler(args.path):
            module_filename = module.__file__
            if module_filename.endswith('.pyc'):
                module_filename = module_filename[:-1]
            with open(module_filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('def '):
                        parts = line.split()
                        if parts[1].startswith('_'):
                            private_functions.append(line)
                        else:
                            public_functions.append(line)
                    elif line.startswith('class '):
                        parts = line.split()
                        if parts[1].startswith('_'):
                            private_classes.append(line)
                        else:
                            public_classes.append(line)

        print 'PUBLIC FUNCTIONS:  {}'.format(len(public_functions))
        print 'PUBLIC CLASSES:    {}'.format(len(public_classes))
        print 'PRIVATE FUNCTIONS: {}'.format(len(private_functions))
        print 'PRIVATE CLASSES:   {}'.format(len(private_classes))

    def setup_argument_parser(self, parser):
        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

