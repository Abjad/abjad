from experimental.developerscripttools.DirectoryScript import DirectoryScript
import os


class ReplacePromptsScript(DirectoryScript):

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def alias(self):
        return 'prompts'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'replace'

    @property
    def short_description(self):
        return 'Replace prompts.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def setup_argument_parser(self, parser):

        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-PA', '--python-to-abjad',
            action='store_const',
            const='python_to_abjad',
            dest='mode',
            help='replace Python (">>>") prompts with Abjad ("abjad>") prompts'
            )

        group.add_argument('-AP', '--abjad-to-python',
            action='store_const',
            const='abjad_to_python',
            dest='mode',
            help='replace Abjad ("abjad>") prompts with Python (">>>") prompts'
            )

