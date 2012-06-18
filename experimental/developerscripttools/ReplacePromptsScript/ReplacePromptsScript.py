from experimental.developerscripttools.DirectoryScript import DirectoryScript
from experimental.developerscripttools.ReplaceInFilesScript import ReplaceInFilesScript
import os


class ReplacePromptsScript(DirectoryScript):

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def alias(self):
        return 'prompts'

    @property
    def long_description(self):
        return '''\
examples:

  Replace Python prompts with Abjad prompts in the current directory:

  $ abj-dev replace prompts --python-to-abjad .

  Replace Abjad prompts with Python prompts in the grandparent directory:

  $ abj-dev replace prompts --abjad-to-python ../..
    '''

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

    def process_args(self, args):
        if args.mode is None:
            print 'No replacement pattern specified, exiting.'

        script = ReplaceInFilesScript()
        arguments = [args.path] + args.mode + ['--force']
        script(arguments)

    def setup_argument_parser(self, parser):

        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-PA', '--python-to-abjad',
            action='store_const',
            const=['>>> ', 'abjad> '],
            dest='mode',
            help='replace Python (">>>") prompts with Abjad ("abjad>") prompts'
            )

        group.add_argument('-AP', '--abjad-to-python',
            action='store_const',
            const=['abjad> ', '>>> '],
            dest='mode',
            help='replace Abjad ("abjad>") prompts with Python (">>>") prompts'
            )

        parser.set_defaults(mode=None)
