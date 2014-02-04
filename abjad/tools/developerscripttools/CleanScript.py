# -*- encoding: utf-8 -*-
import argparse
import os
import shutil
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class CleanScript(DirectoryScript):
    r'''Removes *.pyc, *.swp files and __pycache__ and tmp* directories 
    recursively in a path.

    ..  shell::

        ajv clean --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'clean'``.
        '''
        return 'clean'

    @property
    def long_description(self):
        r'''Long description of scrip.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting groupt of script.

        Returns none.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Clean *.pyc, *.swp, __pycache__ and tmp* files' + \
            ' and folders from PATH.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
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

        for root_directory, directory_names, file_names in os.walk(args.path):
            if '.svn' in directory_names:
                directory_names.remove('.svn')
            extensions = ()
            if args.pyc:
                extensions += ('.pyc',)
            if args.swp:
                extensions += ('.swp',)
            for file_name in file_names:
                if file_name.endswith(extensions):
                    file_path = os.path.join(
                        root_directory,
                        file_name,
                        )
                    os.remove(file_path)
            directories_to_remove = []
            for directory_name in directory_names:
                directory_path = os.path.join(
                    root_directory,
                    directory_name,
                    )
                should_remove = False
                if args.pycache:
                    if directory_name == '__pycache__':
                        should_remove = True
                if args.tmp:
                    if directory_name.startswith('tmp'):
                        should_remove = True
                if not os.listdir(directory_path):
                    should_remove = True
                if should_remove:
                    shutil.rmtree(directory_path)
                    directories_to_remove.append(directory_name)
            for directory_name in directories_to_remove:
                directory_names.remove(directory_name)

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
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
