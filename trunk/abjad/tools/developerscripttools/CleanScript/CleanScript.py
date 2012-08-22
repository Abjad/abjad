from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
import argparse
import os
import shutil


class CleanScript(DirectoryScript):
    '''Remove *.pyc files and __pycache__ and tmp* directories recursively in a path:

    ::

        bash$ ajv clean -h
        usage: clean [-h] [--version] [--pyc] [--pycache] [--tmp] path

        Clean .pyc, __pycache__ and tmp* files and folders from PATH.

        positional arguments:
          path        directory tree to be recursed over

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit
          --pyc       delete .pyc files
          --pycache   delete __pycache__ folders
          --tmp       delete tmp* folders

    Return `CleanScript` instance.
    '''

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'clean'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'Clean .pyc, __pycache__ and tmp* files and folders from PATH.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        if not args.pyc and not args.pycache and not args.tmp:
            args.pyc, args.pycache, args.tmp = True, True, True

        print 'Cleaning...'
        if args.pyc:
            print '\t*.pyc files'
        if args.pycache:
            print '\t__pycache__ directories'
        if args.tmp:
            print '\ttmp* directories'

        for root, dirs, files in os.walk(args.path):

            if '.svn' in dirs:
                dirs.remove('.svn')

            if args.pyc:
                for file in files:
                    if file.endswith('.pyc'):
                        os.remove(os.path.join(root, file))

            to_remove = []

            predicate = lambda x: False
            if args.pycache and args.tmp:
                predicate = lambda x: x == '__pycache__' or x.startswith('tmp')
            elif args.pycache:
                predicate = lambda x: x == '__pycache__'
            elif args.tmp:
                predicate = lambda x: x.startswith('tmp')

            for dir in dirs:
                if predicate(dir):
                    shutil.rmtree(os.path.join(root, dir))
                    to_remove.append(dir)
                
            for dir in to_remove:
                dirs.remove(dir)

    def setup_argument_parser(self, parser):

        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

        parser.add_argument('--pyc',
            action='store_true',
            help='delete .pyc files',
            )

        parser.add_argument('--pycache',
            action='store_true',
            help='delete __pycache__ folders',
            )

        parser.add_argument('--tmp',
            action='store_true',
            help='delete tmp* folders',
            )
