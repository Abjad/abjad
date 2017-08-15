import os
import shutil
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript


class CleanScript(CommandlineScript):
    r'''Removes *.pyc, *.swp files and __pycache__ and tmp* directories
    recursively in a path.

    ..  shell::

        ajv clean --help

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'clean'
    short_description = (
        'Clean *.pyc, *.swp, .cache,  __pycache__ and tmp* '
        'files and folders from PATH.'
        )

    ### PRIVATE METHODS ###

    def _process_args(self, arguments):
        if (not arguments.cache and
            not arguments.pyc and
            not arguments.pycache and
            not arguments.swp and
            not arguments.tmp):
            arguments.cache = True,
            arguments.pyc = True
            arguments.pycache = True
            arguments.swp = True
            arguments.tmp = True
        print('Cleaning...')
        if arguments.pyc:
            print('\t*.pyc files')
        if arguments.swp:
            print('\t*.swp files')
        if arguments.cache:
            print('\t.cache directories')
        if arguments.pycache:
            print('\t__pycache__ directories')
        if arguments.tmp:
            print('\ttmp* directories')

        for root_directory, directory_names, file_names in os.walk(
            arguments.path):
            if '.svn' in directory_names:
                directory_names.remove('.svn')
            extensions = ()
            if arguments.pyc:
                extensions += ('.pyc',)
            if arguments.swp:
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
                directory = os.path.join(
                    root_directory,
                    directory_name,
                    )
                should_remove = False
                if arguments.cache:
                    if directory_name == '.cache':
                        should_remove = True
                if arguments.pycache:
                    if directory_name == '__pycache__':
                        should_remove = True
                if arguments.tmp:
                    if directory_name.startswith('tmp'):
                        should_remove = True
                if not os.listdir(directory):
                    should_remove = True
                if should_remove:
                    shutil.rmtree(directory)
                    directories_to_remove.append(directory_name)
            for directory_name in directories_to_remove:
                directory_names.remove(directory_name)

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )
        parser.add_argument(
            '--cache',
            action='store_true',
            help='delete *.cache folders',
            )
        parser.add_argument(
            '--pyc',
            action='store_true',
            help='delete *.pyc files',
            )
        parser.add_argument(
            '--pycache',
            action='store_true',
            help='delete __pycache__ folders',
            )
        parser.add_argument(
            '--swp',
            action='store_true',
            help='delete Vim *.swp file',
            )
        parser.add_argument(
            '--tmp',
            action='store_true',
            help='delete tmp* folders',
            )
