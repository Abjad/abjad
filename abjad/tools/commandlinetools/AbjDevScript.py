# -*- coding: utf-8 -*-
from __future__ import print_function
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript


class AbjDevScript(CommandlineScript):
    '''`AbjDevScript` is the commandline entry-point to the Abjad
    developer scripts catalog.

    Can be accessed on the commandline via `abj-dev` or `ajv`:

    ..  shell::

        ajv --help

    `ajv` supports subcommands similar to `svn`:

    ..  shell::

        ajv api --help

    '''

    ### CLASS VARIABLES ###

    short_description = 'Entry-point to Abjad developer scripts catalog.'

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        r'''Calls script.
        '''
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
        self._process_args(args)

    ### PRIVATE METHODS ###

    def _handle_help_command(self, unknown_args):
        aliases = self.commandline_script_aliases
        program_names = self.commandline_script_program_names
        commandline_script_class = None
        if len(unknown_args) == 2 and \
            unknown_args[0] in aliases and \
            unknown_args[1] in aliases[unknown_args[0]]:
            commandline_script_class = \
                aliases[unknown_args[0]][unknown_args[1]]
        elif len(unknown_args) == 1 and \
            unknown_args[0] in aliases and \
            not isinstance(aliases[unknown_args[0]], dict):
            commandline_script_class = aliases[unknown_args[0]]
        elif len(unknown_args) == 1 and \
            unknown_args[0] in program_names:
            commandline_script_class = program_names[unknown_args[0]]
        elif not len(unknown_args):
            self(['--help'])
            return
        if commandline_script_class:
            instance = commandline_script_class()
            print(instance.formatted_help)
        else:
            print('Cannot resolve {} to subcommand.'.format(unknown_args))

    def _handle_list_command(self):
        by_scripting_group = {}
        for commandline_script_class in self.commandline_script_classes:
            instance = commandline_script_class()
            scripting_group = getattr(instance, 'scripting_group', None)
            group = by_scripting_group.setdefault(scripting_group, [])
            group.append(instance)
        print()
        if None in by_scripting_group:
            group = by_scripting_group.pop(None)
            for instance in sorted(group, key=lambda x: x.alias):
                message = '{}: {}'.format(
                    instance.alias,
                    instance.short_description,
                    )
                print(message)
            print()
        for group, instances in sorted(by_scripting_group.items()):
            print('[{}]'.format(group))
            for instance in sorted(instances, key=lambda x: x.alias):
                message = '    {}: {}'.format(
                    instance.alias,
                    instance.short_description,
                    )
                print(message)
            print()

    def _process_args(self, args):
        args, unknown_args = args
        if args.subparser_name == 'help':
            self._handle_help_command(unknown_args)
        elif args.subparser_name == 'list':
            self._handle_list_command()
        else:
            if hasattr(args, 'subsubparser_name'):
                commandline_script_class = self.commandline_script_aliases[
                    args.subparser_name][args.subsubparser_name]
            elif getattr(args, 'subparser_name'):
                commandline_script_class = \
                    self.commandline_script_aliases[args.subparser_name]
            elif getattr(args, 'subparser_name') is None:
                self(['--help'])
                return
            instance = commandline_script_class()
            instance(unknown_args)

    def _setup_argument_parser(self, parser):
        subparsers = parser.add_subparsers(
            dest='subparser_name',
            title='subcommands',
            )
        subparsers.add_parser(
            'help',
            add_help=False,
            help='print subcommand help'
            )
        subparsers.add_parser(
            'list',
            add_help=False,
            help='list subcommands',
            )
        alias_map = self.commandline_script_aliases
        for key in sorted(alias_map):
            if not isinstance(alias_map[key], dict):
                commandline_script_class = alias_map[key]
                instance = commandline_script_class()
                subparsers.add_parser(
                    key,
                    add_help=False,
                    help=instance.short_description,
                    )
            else:
                subkeys = sorted(alias_map[key])
                group_subparser = subparsers.add_parser(
                    key,
                    help='{{{}}} subcommand(s)'.format(', '.join(subkeys)),
                    )
                group_subparsers = group_subparser.add_subparsers(
                    dest='subsubparser_name'.format(key),
                    title='{} subcommands'.format(key),
                    )
                for subkey in subkeys:
                    commandline_script_class = alias_map[key][subkey]
                    instance = commandline_script_class()
                    group_subparsers.add_parser(
                        subkey,
                        add_help=False,
                        help=instance.short_description
                        )

    ### PUBLIC PROPERTIES ###

    @property
    def commandline_script_aliases(self):
        r'''Developer script aliases.
        '''
        scripting_groups = []
        aliases = {}
        for commandline_script_class in self.commandline_script_classes:
            instance = commandline_script_class()
            if getattr(instance, 'alias', None):
                scripting_group = getattr(instance, 'scripting_group', None)
                if scripting_group:
                    scripting_groups.append(scripting_group)
                    entry = (scripting_group, instance.alias)
                    if (scripting_group,) in aliases:
                        message = 'alias conflict between scripting group'
                        message += ' {!r} and {}'
                        message = message.format(
                            scripting_group,
                            aliases[(scripting_group,)].__name__,
                            )
                        raise Exception(message)
                    if entry in aliases:
                        message = 'alias conflict between {} and {}'
                        message = message.format(
                            aliases[entry].__name__,
                            commandline_script_class.__name__,
                            )
                        raise Exception(message)
                    aliases[entry] = commandline_script_class
                else:
                    entry = (instance.alias,)
                    if entry in scripting_groups:
                        message = 'alias conflict between {}'
                        message += ' and scripting group {!r}'
                        message = message.format(
                            commandline_script_class.__name__,
                            instance.alias,
                            )
                        raise Exception(message)
                    if entry in aliases:
                        message = 'alias conflict be {} and {}'
                        message = message.format(
                            commandline_script_class.__name__,
                            aliases[entry],
                            )
                        raise Exception(message)
                    aliases[(instance.alias,)] = commandline_script_class
            else:
                if instance.program_name in scripting_groups:
                    message = 'Alias conflict between {}'
                    message += ' and scripting group {!r}'
                    message = message.format(
                        commandline_script_class.__name__,
                        instance.program_name,
                        )
                    raise Exception(message)
                aliases[(instance.program_name,)] = commandline_script_class
        alias_map = {}
        for key, value in aliases.items():
            if len(key) == 1:
                alias_map[key[0]] = value
            else:
                if key[0] not in alias_map:
                    alias_map[key[0]] = {}
                alias_map[key[0]][key[1]] = value
        return alias_map

    @property
    def commandline_script_classes(self):
        r'''Developer scripts classes.
        '''
        classes = self.list_commandline_script_classes()
        classes.remove(type(self))
        return classes

    @property
    def commandline_script_program_names(self):
        r'''Developer script program names.
        '''
        program_names = {}
        for commandline_script_class in self.commandline_script_classes:
            instance = commandline_script_class()
            program_names[instance.program_name] = commandline_script_class
        return program_names
