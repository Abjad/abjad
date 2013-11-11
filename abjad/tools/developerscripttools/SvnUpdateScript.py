# -*- encoding: utf-8 -*-
import argparse
import os
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
from abjad.tools.developerscripttools.CleanScript import CleanScript


class SvnUpdateScript(DirectoryScript):
    r'''Run `svn up` on various Abjad paths:

    ..  shell::

        ajv svn up --help

    It is usually most useful to run the script with the `--clean` flag, 
    in case there are incoming deletes, as `svn` will not delete 
    directories containing unversioned files, such as .pyc:

    ::

        bash$ ajv svn up -C -R

    Return `SvnUpdateScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'up'

    @property
    def long_description(self):
        return 'If no path flag is specified,' + \
            ' the current directory will be updated.'

    @property
    def scripting_group(self):
        return 'svn'

    @property
    def short_description(self):
        return '"svn update" various paths.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):

        if args.clean:
            clean_args = [args.path]
            clean_script = CleanScript()
            clean_script(clean_args)

        print 'Updating...'
        systemtools.IOManager.spawn_subprocess('svn update {}'.format(args.path))

    def setup_argument_parser(self, parser):

        from abjad import abjad_configuration

        parser.add_argument('-C', '--clean',
            action='store_true',
            help='remove .pyc files and __pycache__ directories before updating'
            )

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-P', '--path',
            dest='path',
            help='update the path PATH',
            #metavar='X',
            type=self._validate_path,
            )

        group.add_argument('-E', '--experimental',
            action='store_const',
            const=abjad_configuration.abjad_experimental_directory_path,
            dest='path',
            help='update Abjad abjad.tools directory',
            )

        group.add_argument('-M', '--mainline',
            action='store_const',
            const=abjad_configuration.abjad_directory_path,
            dest='path',
            help='update Abjad mainline directory',
            )

        group.add_argument('-R', '--root',
            action='store_const',
            const=abjad_configuration.abjad_root_directory_path,
            dest='path',
            help='update Abjad root directory',
            )

        parser.set_defaults(path=os.path.abspath(os.path.curdir))
