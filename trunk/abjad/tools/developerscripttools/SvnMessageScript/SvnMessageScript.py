from abjad.tools import configurationtools
from abjad.tools import iotools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript
import os


class SvnMessageScript(DeveloperScript):
    '''Edit a temporary `svn` commit message, stored in the `.abjad` directory:

    ::

        bash$ ajv svn msg -h
        usage: svn-message [-h] [--version] [-C]

        Write commit message for future commit usage.

        optional arguments:
          -h, --help   show this help message and exit
          --version    show program's version number and exit
          -C, --clean  delete previous commit message before editing

    Return `SvnMessageScript` instance.
    '''

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'msg'

    @property
    def commit_message_path(self):
        from abjad import ABJCFG
        commit_file = 'abjad_commit.txt'
        commit_path = os.path.join(ABJCFG.ABJAD_CONFIG_DIRECTORY_PATH, commit_file)
        return commit_path

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'svn'

    @property
    def short_description(self):
        return 'Write commit message for future commit usage.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        text_editor = configurationtools.get_text_editor()
        if args.clean:
            if os.path.exists(self.commit_message_path):
                os.remove(self.commit_message_path)
        command = '{} {}'.format(text_editor, self.commit_message_path)
        iotools.spawn_subprocess(command)

    def setup_argument_parser(self, parser):
        parser.add_argument('-C', '--clean',
            action='store_true',
            help='delete previous commit message before editing'
            )
