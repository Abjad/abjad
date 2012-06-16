from abjad.cfg.cfg import ABJADPATH, EXPERIMENTALPATH, ROOTPATH
from abjad.tools import iotools
from experimental.developerscripttools.DirectoryScript import DirectoryScript
from experimental.developerscripttools.CleanScript import CleanScript
import argparse
import os


class SvnUpdateScript(DirectoryScript):

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'up'

    @property
    def long_description(self):
        return None

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
            clean_args = ['--pyc', '--pycache', '--tmp', args.path]
            clean_script = CleanScript()
            clean_script(clean_args)
        iotools.spawn_subprocess('svn update {}'.format(args.path))

    def setup_argument_parser(self, parser):

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
            const=EXPERIMENTALPATH,
            dest='path',
            help='update Abjad experimental directory',
            )

        group.add_argument('-M', '--mainline',
            action='store_const',
            const=ABJADPATH,
            dest='path',
            help='update Abjad mainline directory',
            )

        group.add_argument('-R', '--root',
            action='store_const',
            const=ROOTPATH,
            dest='path',
            help='update Abjad root directory',
            )

        parser.set_defaults(path=os.path.abspath(os.path.curdir))
