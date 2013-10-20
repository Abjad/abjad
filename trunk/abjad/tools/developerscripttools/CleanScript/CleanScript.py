# -*- encoding: utf-8 -*-
import argparse
import os
import shutil
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class CleanScript(DirectoryScript):
    r'''Remove *.pyc, *.swp files and __pycache__ and tmp* directories 
    recursively in a path:

    ..  shell::

        ajv clean --help

    Return `CleanScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

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
        return 'Clean *.pyc, *.swp, __pycache__ and tmp* files' + \
            ' and folders from PATH.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        if not args.pyc and not args.pycache and \
            not args.swp and not args.tmp:
            args.pyc, args.pycache, args.swp, args.tmp = True, True, True, True

        print 'Cleaning...'
        if args.pyc:
            print '\t*.pyc files'
        if args.swp:
            print '\t*.swp files'
        if args.pycache:
            print '\t__pycache__ directories'
        if args.tmp:
            print '\ttmp* directories'

        for root, dirs, files in os.walk(args.path):
            if '.svn' in dirs:
                dirs.remove('.svn')

            extensions = ()
            if args.pyc:
                extensions += ('.pyc',)
            if args.swp:
                extensions += ('.swp',)
            for file in files:
                if file.endswith(extensions):
                    os.remove(os.path.join(root, file))

            directories_to_remove = []
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
                    directories_to_remove.append(dir)
            for dir in directories_to_remove:
                dirs.remove(dir)

    def setup_argument_parser(self, parser):
        parser.add_argument('path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )
        parser.add_argument('--pyc',
            action='store_true',
            help='delete *.pyc files',
            )
        parser.add_argument('--pycache',
            action='store_true',
            help='delete __pycache__ folders',
            )
        parser.add_argument('--swp',
            action='store_true',
            help='delete Vim *.swp file',
            )
        parser.add_argument('--tmp',
            action='store_true',
            help='delete tmp* folders',
            )
