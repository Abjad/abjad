# -*- encoding: utf-8 -*-
import argparse
import os
from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class AbjDevScript(DeveloperScript):
    '''`AbjDevScript` is the commandline entry-point to the Abjad 
    developer scripts catalog.

    Can be accessed on the commandline via `abj-dev` or `ajv`:

    ..  shell::

        ajv --help

    `ajv` supports subcommands similar to `svn`:

    ..  shell::

        ajv api --help

    Return `AbjDevScript` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        if args is None:
            args = self.argument_parser.parse_known_args()
        else:
            if isinstance(args, str):
                args = args.split()
            elif not isinstance(args, (list, tuple)):
                message = 'must be str, list, tuple or none: {!r}.'
                message = message.format(args)
                raise ValueError(message)
            args = self.argument_parser.parse_known_args(args)
        self.process_args(args)

    ### PUBLIC PROPERTIES ###

    @property
    def developer_script_aliases(self):
        scripting_groups = []
        aliases = {}
        for developer_script_class in self.developer_script_classes:
            instance = developer_script_class()

            if instance.alias is not None:

                if instance.scripting_group is not None:
                    scripting_groups.append(instance.scripting_group)
                    entry = (instance.scripting_group, instance.alias)
                    if (instance.scripting_group,) in aliases:
                        message = 'alias conflict between scripting group'
                        message += ' {!r} and {}'
                        message = message.format(
                            instance.scripting_group, 
                            aliases[(instance.scripting_group,)].__name__,
                            )
                        raise Exception(message)
                    if entry in aliases:
                        message = 'alias conflict between {} and {}'
                        message = message.format(
                            aliases[entry].__name__,
                            developer_script_class.__name__,
                            )
                        raise Exception(message)
                    aliases[entry] = developer_script_class

                else:
                    entry = (instance.alias,)
                    if entry in scripting_groups:
                        message = 'alias conflict between {}'
                        message += ' and scripting group {!r}'
                        message = message.format(
                            developer_script_class.__name__, 
                            instance.alias,
                            )
                        raise Exception(message)
                    if entry in aliases:
                        message = 'alias conflict be {} and {}'
                        message = message.format(
                            developer_script_class.__name__, 
                            aliases[entry],
                            )
                        raise Exception(message)
                    aliases[(instance.alias,)] = developer_script_class

            else:
                if instance.program_name in scripting_groups:
                    message = 'Alias conflict between {}'
                    message += ' and scripting group {!r}'
                    message = message.format(
                        developer_script_class.__name__, 
                        instance.program_name,
                        )
                    raise Exception(message)
                aliases[(instance.program_name,)] = developer_script_class

        aliasdict = {}

        for key, value in aliases.iteritems():
            if len(key) == 1:
                aliasdict[key[0]] = value
            else:
                if key[0] not in aliasdict:
                    aliasdict[key[0]] = { }
                aliasdict[key[0]][key[1]] = value

        return aliasdict

    @property
    def developer_script_classes(self):
        from abjad.tools import developerscripttools
        classes = developerscripttools.get_developer_script_classes()
        classes.remove(type(self))
        return classes

    @property
    def developer_script_program_names(self):
        program_names = {}
        for developer_script_class in self.developer_script_classes:
            instance = developer_script_class()
            program_names[instance.program_name] = developer_script_class
        return program_names

    @property
    def long_description(self):
        return None

    @property
    def short_description(self):
        return 'Entry-point to Abjad developer scripts catalog.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        args, unknown_args = args

        if args.subparser_name == 'help':
            aliases = self.developer_script_aliases
            program_names = self.developer_script_program_names
            developer_script_class = None
            if len(unknown_args) == 2 and \
                unknown_args[0] in aliases and \
                unknown_args[1] in aliases[unknown_args[0]]:
                developer_script_class = \
                    aliases[unknown_args[0]][unknown_args[1]]
            elif len(unknown_args) == 1 and \
                unknown_args[0] in aliases and \
                not isinstance(aliases[unknown_args[0]], dict):
                developer_script_class = aliases[unknown_args[0]]
            elif len(unknown_args) == 1 and \
                unknown_args[0] in program_names:
                developer_script_class = program_names[unknown_args[0]]

            if developer_script_class:
                instance = developer_script_class()
                print instance.formatted_help
            else:
                print 'Cannot resolve {} to subcommand.'.format(unknown_args)

        elif args.subparser_name == 'list':
            entries = []
            for developer_script_class in self.developer_script_classes:
                instance = developer_script_class()
                alias = ''
                if instance.alias is not None:
                    if instance.scripting_group is not None:
                        alias = '\n[{} {}]'.format(
                            instance.scripting_group, instance.alias)
                    else:
                        alias = '\n[{}]'.format(instance.alias)
                entries.append('{}{}\n\t{}'.format(
                    instance.program_name, alias, instance.short_description))
            print ''
            print '\n\n'.join(entries)
            print ''

        else:
            if hasattr(args, 'subsubparser_name'):
                developer_script_class = self.developer_script_aliases[
                    args.subparser_name][args.subsubparser_name]
            else:
                developer_script_class = \
                    self.developer_script_aliases[args.subparser_name]
            instance = developer_script_class()
            instance(unknown_args)

    def setup_argument_parser(self, parser):

        subparsers = parser.add_subparsers(
            dest='subparser_name',
            title='subcommands',
            )

        info_subparser = subparsers.add_parser('help',
            add_help=False,
            help='print subcommand help'
            )

        list_subparser = subparsers.add_parser('list',
            add_help=False,
            help='list subcommands',
            )

        aliasdict = self.developer_script_aliases
        for key in sorted(aliasdict):
            if not isinstance(aliasdict[key], dict):
                developer_script_class = aliasdict[key]
                instance = developer_script_class()
                class_subparser = subparsers.add_parser(key,
                    add_help=False,
                    help=instance.short_description,
                    )
            else:
                group_subparser = subparsers.add_parser(key,
                    help='"{}"-related subcommands'.format(key),
                    )
                group_subparsers = group_subparser.add_subparsers(
                    dest='subsubparser_name'.format(key),
                    title='{} subcommands'.format(key),
                    )
                for subkey in sorted(aliasdict[key]):
                    developer_script_class = aliasdict[key][subkey]
                    instance = developer_script_class()
                    group_subparsers.add_parser(subkey,
                        add_help=False,
                        help=instance.short_description
                        )
