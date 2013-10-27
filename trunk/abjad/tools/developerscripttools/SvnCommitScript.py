# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
from abjad.tools.developerscripttools.SvnMessageScript import SvnMessageScript


class SvnCommitScript(DirectoryScript):
    r'''Run `svn commit`, using the commit message stored in the 
    `.abjad` directory.

    The commit message will be printed to the terminal, and must be manually
    accepted or rejected before proceeding:

    ..  shell::

        ajv svn ci --help

    Return `SvnCommitScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

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
        from abjad import abjad_configuration
        commit_file = 'abjad_commit.txt'
        commit_path = os.path.join(
            abjad_configuration.abjad_configuration_directory_path, 
            commit_file)

        while not os.path.exists(commit_path):
            SvnMessageScript()()

        commit_command = 'svn commit {} -F {}'.format(args.path, commit_path)

        while True:
            print '\nSTORED COMMIT MESSAGE:\n'
            with open(commit_path, 'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    print '~ {}'.format(line)
            print
            result = raw_input(
                'Accept [Y], Reject [n], Abort [a]: ').strip().lower()
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
            default=os.getcwd(),
            help='commit the path PATH',
            nargs='?',
            type=self._validate_path,
            )
