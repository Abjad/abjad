# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import os
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class NewScoreScript(DirectoryScript):
    r'''Makes a new score package in the current directory.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.
        '''
        return 'new'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Make score package.'

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
        if not args.path:
            path = stringtools.to_accent_free_snake_case(args.title)
        else:
            path = args.path
        if not os.path.isabs(path):
            current_directory = os.path.curdir
            path = os.path.join(current_directory, path)
        if os.path.exists(path):
            message = 'FAILED: Directory {!r} already exists.'
            message = message.format(path)
            print(message)
            sys.exit(1)
        systemtools.IOManager._make_score_package(
            path,
            args.title,
            args.year,
            args.composer_name,
            args.composer_email,
            args.composer_github,
            args.composer_library
            )

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        parser.add_argument(
            'title',
            help='score title',
            )
        parser.add_argument(
            '-P', '--path',
            metavar='PATH',
            )
        parser.add_argument(
            '-Y', '--year',
            default=str(datetime.datetime.today().year),
            metavar='YEAR',
            )
        parser.add_argument(
            '-N', '--composer-name',
            default='A Composer',
            metavar='NAME',
            )
        parser.add_argument(
            '-E', '--composer-email',
            default='composer@email.com',
            metavar='EMAIL',
            )
        parser.add_argument(
            '-G', '--composer-github',
            default='composer',
            metavar='GITHUB_USERNAME',
            )
        parser.add_argument(
            '-L', '--composer-library',
            default='library',
            metavar='LIBRARY_NAME',
            )
