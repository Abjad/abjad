# -*- encoding: utf-8 -*-
import argparse
import os
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
from abjad.tools.developerscripttools.CleanScript import CleanScript


class AbjGrepScript(DirectoryScript):
    r'''Runs `grep` against a path, ignoring `svn` and docs-related files.

    ..  shell::

        ajv grep --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'grep'``.
        '''
        return 'grep'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string.
        '''
        return '''\
If no PATH flag is specified, the current directory will be searched.
    '''

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
        return 'grep PATTERN in PATH'

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

        systemtools.IOManager.clear_terminal()
        if args.whole_words_only:
            whole_words_only = '-w'
        else:
            whole_words_only = ''
        command = r'grep {} -Irn {!r} {} | grep -v svn-base | grep -v svn\/ | grep -v docs'.format(
            whole_words_only, args.pattern, os.path.relpath(args.path))
        systemtools.IOManager.spawn_subprocess(command)

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''

        from abjad import abjad_configuration

        parser.add_argument('pattern',
            help='pattern to search for'
            )

        parser.add_argument('-W', '--whole-words-only',
            action='store_true',
            help='''match only whole words, similar to grep's "-w" flag''',
            )

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-P', '--path',
            dest='path',
            help='grep PATH',
            type=self._validate_path,
            )

        group.add_argument('-X', '--experimental',
            action='store_const',
            const=abjad_configuration.abjad_experimental_directory_path,
            dest='path',
            help='grep Abjad abjad.tools directory',
            )

        group.add_argument('-M', '--mainline',
            action='store_const',
            const=abjad_configuration.abjad_directory_path,
            dest='path',
            help='grep Abjad mainline directory',
            )

        group.add_argument('-T', '--tools',
            action='store_const',
            const=os.path.join(
                abjad_configuration.abjad_directory_path, 'tools'),
            dest='path',
            help='grep Abjad mainline tools directory',
            )

        group.add_argument('-R', '--root',
            action='store_const',
            const=abjad_configuration.abjad_root_directory_path,
            dest='path',
            help='grep Abjad root directory',
            )

        parser.set_defaults(path=os.path.abspath(os.path.curdir))
