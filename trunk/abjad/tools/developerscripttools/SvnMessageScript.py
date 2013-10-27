# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class SvnMessageScript(DeveloperScript):
    r'''Edit a temporary `svn` commit message, stored in the `.abjad` 
    directory:

    ..  shell::

        ajv svn msg --help

    Return `SvnMessageScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'msg'

    @property
    def commit_message_path(self):
        from abjad import abjad_configuration
        commit_file = 'abjad_commit.txt'
        commit_path = os.path.join(
            abjad_configuration.abjad_configuration_directory_path, 
            commit_file)
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
        from abjad import abjad_configuration
        text_editor = abjad_configuration.get_text_editor()
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
