from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
from abjad.tools.developerscripttools.ReplaceInFilesScript import ReplaceInFilesScript
import os


class ReplacePromptsScript(DirectoryScript):
    '''Replace prompts in code examples recursively:

    ::

        bash$ ajv replace prompts -h
        usage: replace-prompts [-h] [--version] [-PA | -AP] path

        Replace prompts.

        positional arguments:
          path                  directory tree to be recursed over

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit
          -PA, --python-to-abjad
                                replace Python (">>>") prompts with Abjad ("abjad>")
                                prompts
          -AP, --abjad-to-python
                                replace Abjad ("abjad>") prompts with Python (">>>")
                                prompts

        examples:

          Replace Python prompts with Abjad prompts in the current directory:

          $ abj-dev replace prompts --python-to-abjad .

          Replace Abjad prompts with Python prompts in the grandparent directory:

          $ abj-dev replace prompts --abjad-to-python ../..
            
    `ReplacePromptsScript` uses `ReplaceInFilesScript` for its replacement functionality.

    Return `ReplacePromptsScript` instance.
    '''

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
