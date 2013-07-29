import argparse
import os
from abjad.tools import documentationtools
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


class AbjDevScript(DeveloperScript):
    '''`AbjDevScript` is the commandline entry-point to the Abjad 
    developer scripts catalog.

    Can be accessed on the commandline via `abj-dev` or `ajv`:

    ::

        bash$ abj-dev
        usage: abj-dev [-h] [--version]

                       {help, list, api, book, clean, count, doctest, grep, new, rename, replace, svn}
                       ...

        Entry-point to Abjad developer scripts catalog.

        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit

        subcommands:
          {help,list,api,book,clean,count,doctest,grep,new,rename,replace,svn}
            help                print subcommand help
            list                list subcommands
            api                 Build the Abjad APIs.
            book                Preprocess HTML, LaTeX or ReST source with Abjad.
            clean               Clean .pyc, __pycache__ and tmp* files and folders
                                from PATH.
            count               "count"-related subcommands
            doctest             Run doctests on all modules in current path.
            grep                grep PATTERN in PATH
            new                 "new"-related subcommands
            rename              Rename public modules.
            replace             "replace"-related subcommands
            svn                 "svn"-related subcommands

    `ajv` supports subcommands similar to `svn`:

    ::

        bash$ ajv count -h
        usage: abj-dev count [-h] {linewidths,tools} ...

        optional arguments:
          -h, --help          show this help message and exit

        count subcommands:
          {linewidths,tools}
            linewidths        Count maximum line-width of all modules in PATH.
            tools             Count tools in PATH.

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
                raise ValueError
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
                        message = 'Alias conflict between scripting group'
                        message += ' {!r} and {}'
                        raise Exception(message.format(
                            instance.scripting_group, 
                            aliases[(instance.scripting_group,)].__name__))
                    if entry in aliases:
                        message = 'Alias conflict between {} and {}'
                        raise Exception(message.format(
                            aliases[entry].__name__ and \
                                developer_script_class.__name__))
                    aliases[entry] = developer_script_class

                else:
                    entry = (instance.alias,)
                    if entry in scripting_groups:
                        message = 'Alias conflict between {}'
                        message += ' and scripting group {!r}'
                        raise Exception(message.format(
                            developer_script_class.__name__, instance.alias))
                    if entry in aliases:
                        raise Exception('Alias conflict be {} and {}'.format(
                            developer_script_class.__name__, aliases[entry]))
                    aliases[(instance.alias,)] = developer_script_class

            else:
                if instance.program_name in scripting_groups:
                    message = 'Alias conflict between {}'
                    message += ' and scripting group {!r}'
                    raise Exception(message.format(
                        developer_script_class.__name__, 
                        instance.program_name))
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
        classes.remove(self.__class__)
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
