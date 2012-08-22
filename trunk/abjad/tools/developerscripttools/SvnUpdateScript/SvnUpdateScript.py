from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
from abjad.tools.developerscripttools.CleanScript import CleanScript
import argparse
import os


class SvnUpdateScript(DirectoryScript):
    '''Run `svn up` on various Abjad paths:

    ::

        bash$ ajv svn up -h
        usage: svn-update [-h] [--version] [-C] [-P PATH | -E | -M | -R]

        "svn update" various paths.

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit
          -C, --clean           remove .pyc files and __pycache__ directories before
                                updating
          -P PATH, --path PATH  update the path PATH
          -E, --abjad.tools    update Abjad abjad.tools directory
          -M, --mainline        update Abjad mainline directory
          -R, --root            update Abjad root directory

        If no path flag is specified, the current directory will be updated.

    It is usually most useful to run the script with the `--clean` flag, in case
    there are incoming deletes, as `svn` will not delete directories containing
    unversioned files, such as .pyc:

    ::

        bash$ ajv svn up -C -R

    Return `SvnUpdateScript` instance.
    '''

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'up'

    @property
    def long_description(self):
        return 'If no path flag is specified, the current directory will be updated.'

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

        print 'Updating...'
        iotools.spawn_subprocess('svn update {}'.format(args.path))

    def setup_argument_parser(self, parser):

        from abjad import ABJCFG

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
            const=ABJCFG.ABJAD_EXPERIMENTAL_PATH,
            dest='path',
            help='update Abjad abjad.tools directory',
            )

        group.add_argument('-M', '--mainline',
            action='store_const',
            const=ABJCFG.ABJAD_PATH,
            dest='path',
            help='update Abjad mainline directory',
            )

        group.add_argument('-R', '--root',
            action='store_const',
            const=ABJCFG.ABJAD_ROOT_PATH,
            dest='path',
            help='update Abjad root directory',
            )

        parser.set_defaults(path=os.path.abspath(os.path.curdir))
