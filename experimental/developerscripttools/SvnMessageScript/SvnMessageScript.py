from abjad.tools import configurationtools
from abjad.tools import iotools
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import os


class SvnMessageScript(DeveloperScript):

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'msg'

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
        HOME = dict(configurationtools.list_abjad_environment_variables())['HOME']
        commit_file = 'abjad_commit.txt'
        commit_path = os.path.join(HOME, '.abjad', commit_file)
        text_editor = configurationtools.get_text_editor()
        if args.clean:
            if os.path.exists(commit_path):
                os.remove(commit_path)
        command = '{} {}'.format(text_editor, commit_path)
        iotools.spawn_subprocess(command)

    def setup_argument_parser(self, parser):
        parser.add_argument('-C', '--clean',
            action='store_true',
            help='delete previous commit message before editing'
            )
