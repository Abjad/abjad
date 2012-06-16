from experimental.developerscripttools.DirectoryScript import DirectoryScript
import os


class ReplaceInFilesScript(DirectoryScript):

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def alias(self):
        return 'text'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'replace'

    @property
    def short_description(self):
        return 'Replace text.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def setup_argument_parser(self, parser):

        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

        parser.add_argument('old',
            help='old text',
            )

        parser.add_argument('new',
            help='new text',
            )

        parser.add_argument('--force',
            action='store_true',
            help='force "yes" to every replacement'
            )
