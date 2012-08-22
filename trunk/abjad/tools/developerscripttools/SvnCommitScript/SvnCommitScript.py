from abjad.tools import configurationtools
from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
from abjad.tools.developerscripttools.SvnMessageScript import SvnMessageScript
import os


class SvnCommitScript(DirectoryScript):
    '''Run `svn commit`, using the commit message stored in the `.abjad` directory.

    The commit message will be printed to the terminal, and must be manually
    accepted or rejected before proceeding:

    ::

        bash$ ajv svn ci -h
        usage: svn-commit [-h] [--version] path

        "svn commit", using previously written commit message.

        positional arguments:
          path        commit the path PATH

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit

    Return `SvnCommitScript` instance.
    '''

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'ci'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'svn'

    @property
    def short_description(self):
        return '"svn commit", using previously written commit message.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        from abjad import ABJCFG
        commit_file = 'abjad_commit.txt'
        commit_path = os.path.join(ABJCFG.ABJAD_CONFIG_DIRECTORY_PATH, commit_file)

        while not os.path.exists(commit_path):
            SvnMessageScript()()

        commit_command = 'svn commit {} -F {}'.format(args.path, commit_path)

        while True:
            print '\nSTORED COMMIT MESSAGE:\n'
            with open(commit_path, 'r') as f:
                print f.read()
            result = raw_input('Accept [Y], Reject [n], Abort [a]: ').strip().lower()
            if result in ('', 'y', 'yes'):
                iotools.spawn_subprocess(commit_command)
                return
            elif result in ('n', 'no'):
                SvnMessageScript()()
            elif result in ('a', 'abort'):
                return
            else:
                print 'Invalid response {!r}, repeating...'.format(result)
            

    def setup_argument_parser(self, parser):
        parser.add_argument('path',
            help='commit the path PATH',
            type=self._validate_path,
            )

