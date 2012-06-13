from abjad.tools import documentationtools
from experimental.developerscripttools.DeveloperScript import DeveloperScript
from experimental.developerscripttools.get_developer_script_classes import get_developer_script_classes
import argparse
import os


class AbjDevScript(DeveloperScript):

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        if args is None:
            args = self.argument_parser.parse_known_args()
        else:
            if isinstance(args, str):
                args = args.split()
            elif not isinstance(args, (list, tuple)):
                raise ValueError
            args = self.argument_parser.parse_known_args(args)
        self._process_args(args)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def long_description(self):
        return None

    @property
    def developer_script_aliases(self):
        aliases = {}
        for klass in self.developer_script_classes:
            aliases[klass().program_name] = klass
        return aliases

    @property
    def developer_script_classes(self):
        klasses = get_developer_script_classes()
        klasses.remove(self.__class__)
        return klasses

    @property
    def short_description(self):
        return 'Entry-point to Abjad developer scripts catalog.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        args, unknown_args = args

        if args.subparser_name == 'info':
            instance = self.developer_script_aliases[args.subcommand]()
            print instance.formatted_help

        elif args.subparser_name == 'list':
            for klass in self.developer_script_classes:
                instance = klass()
                print '{}:\n\t{}'.format(instance.program_name, instance.short_description)

        else:
            klass = self.developer_script_aliases[args.subparser_name]
            instance = klass()
            instance(unknown_args)

    def _setup_argument_parser(self, parser):
        subparsers = parser.add_subparsers(
            dest='subparser_name',
            help='subcommand help',
            title='subcommands',
            )
        
        info_subparser = subparsers.add_parser('info',
            help='print subcommand info')
        info_subparser.add_argument('subcommand',
            choices=self.developer_script_aliases.keys(),
            help='subcommand name',
            )

        list_subparser = subparsers.add_parser('list',
            help='list subcommands',
            )

        klasses = get_developer_script_classes()
        klasses.remove(self.__class__)
        for klass in klasses:
            instance = klass()
            klass_subparser = subparsers.add_parser(instance.program_name,
                help=instance.short_description
                )
