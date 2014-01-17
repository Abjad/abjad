# -*- encoding: utf-8 -*-
import abc
import argparse
import os
from abjad.tools import abctools
from abjad.tools import stringtools


class DeveloperScript(abctools.AbjadObject):
    r'''Object-oriented model of a developer script.

    `DeveloperScript` is the abstract parent from which concrete developer
    scripts inherit.

    Developer scripts can be called from the command line, generally via the
    `ajv` command.

    Developer scripts can be instantiated by other developer scripts in order
    to share functionality.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_argument_parser',
        )

    ### INITIALIZER ###

    def __init__(self):
        parser = self._argument_parser = argparse.ArgumentParser(
            description=self.short_description,
            epilog=self.long_description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=self.program_name,
            )
        parser.add_argument('--version', action='version',
            version='%(prog)s {}'.format(self.version))
        self._argument_parser = parser
        self.setup_argument_parser(parser)

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        r'''Calls developer script.

        Returns none.
        '''
        if args is None:
            args = self.argument_parser.parse_args()
        else:
            if isinstance(args, str):
                args = args.split()
            elif not isinstance(args, (list, tuple)):
                raise ValueError
            args = self.argument_parser.parse_args(args)
        self.process_args(args)

    def __getstate__(self):
        r'''Gets object state.
        '''
        return {}

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''The alias to use for the script, useful only if the script defines
        an abj-dev scripting group as well.
        '''
        return None

    @property
    def argument_parser(self):
        r'''The script's instance of argparse.ArgumentParser.
        '''
        return self._argument_parser

    @property
    def colors(self):
        r'''Colors.

        Returns dictionary.
        '''
        return {
            'BLUE': '\033[94m',
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'END': '\033[0m',
            }

    @property
    def formatted_help(self):
        r'''Formatted help of developer script.
        '''
        return self._argument_parser.format_help()

    @property
    def formatted_usage(self):
        r'''Formatted usage of developer script.
        '''
        return self._argument_parser.format_usage()

    @property
    def formatted_version(self):
        r'''Formatted version of developer script.
        '''
        return self._argument_parser.format_version()

    @abc.abstractproperty
    def long_description(self):
        r'''The long description, printed after arguments explanations.
        '''
        raise NotImplementedError

    @property
    def program_name(self):
        r'''The name of the script, callable from the command line.
        '''
        name = type(self).__name__[:type(self).__name__.rfind('Script')]
        return stringtools.upper_camel_case_to_space_delimited_lowercase(
            name).replace(' ', '-')

    @property
    def scripting_group(self):
        r'''Scripting subcommand group of script.
        '''
        return None

    @abc.abstractproperty
    def short_description(self):
        r'''Short description of the script, printed before arguments
        explanations.

        Also used as a summary in other contexts.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def version(self):
        r'''Version number of developer script.
        '''
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def process_args(self, args):
        r'''Processes `args`.
        '''
        pass

    @abc.abstractmethod
    def setup_argument_parser(self):
        r'''Sets up argument parser.
        '''
        pass
