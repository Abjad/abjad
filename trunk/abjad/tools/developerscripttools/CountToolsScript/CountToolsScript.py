from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
import argparse
import importlib
import os


class CountToolsScript(DirectoryScript):
    '''Count public and private functions and classes in a path:

    ::

        bash$ ajv count tools -h
        usage: count-tools [-h] [--version] path

        Count tools in PATH.

        positional arguments:
          path        directory tree to be recursed over

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit

    Return `CountToolsScript` instance.
    '''

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

    ### PUBLIC METHODS ###

    def process_args(self, args):

        private_classes = []
        private_functions = []
        public_classes = []
        public_functions = []

        crawler = documentationtools.ModuleCrawler(args.path,
            visit_private_modules=True)
        for module in crawler:
            module_filename = module.__file__
            if module_filename.endswith('.pyc'):
                module_filename = module_filename[:-1]
            with open(module_filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('def '):
                        name = line.split()[1].partition('(')[0]
                        payload = (name, os.path.relpath(module_filename))
                        if name.startswith('_'):
                            private_functions.append(payload)
                        else:
                            public_functions.append(payload)
                    elif line.startswith('class '):
                        name = line.split()[1].partition('(')[0]
                        payload = (name, os.path.relpath(module_filename))
                        if name.startswith('_'):
                            private_classes.append(payload)
                        else:
                            public_classes.append(payload)

        print 'PUBLIC FUNCTIONS:  {}'.format(len(public_functions))
        print 'PUBLIC CLASSES:    {}'.format(len(public_classes))
        print 'PRIVATE FUNCTIONS: {}'.format(len(private_functions))
        if args.verbose:
            for x in private_functions:
                name, filename = x
                print '\t{}:'.format(filename)
                print '\t\t{}'.format(name)
        print 'PRIVATE CLASSES:   {}'.format(len(private_classes))
        if args.verbose:
            for x in private_classes:
                name, filename = x
                print '\t{}:'.format(filename)
                print '\t\t{}'.format(name)

    def setup_argument_parser(self, parser):
        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )
        parser.add_argument('-v', '--verbose',
            action='store_true',
            help='print verbose information',
            )

