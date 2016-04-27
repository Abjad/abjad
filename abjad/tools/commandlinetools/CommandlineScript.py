# -*- coding: utf-8 -*-
from __future__ import print_function
import abc
import argparse
import inspect
import os
from abjad.tools import abctools
from abjad.tools import documentationtools
from abjad.tools import stringtools


class CommandlineScript(abctools.AbjadObject):
    r'''Object-oriented model of a developer script.

    `CommandlineScript` is the abstract parent from which concrete developer
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

    _colors = {
        'BLUE': '\033[94m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'END': '\033[0m',
        }

    ### INITIALIZER ###

    def __init__(self):
        short_description = getattr(self, 'short_description', None)
        long_description = getattr(self, 'long_description', None)
        if long_description:
            long_description = stringtools.normalize(long_description)
        parser = self._argument_parser = argparse.ArgumentParser(
            description=short_description,
            epilog=long_description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=self.program_name,
            )
        version = '%(prog)s {}'
        version = version.format(getattr(self, 'version', 1.0))
        parser.add_argument('--version', action='version', version=version)
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

    ### PRIVATE METHODS ###

    def _is_valid_path(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
        return False

    def _validate_path(self, path):
        message = '{!r} is not a valid directory.'
        message = message.format(path)
        error = argparse.ArgumentTypeError(message)
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return os.path.relpath(path)

    ### PUBLIC PROPERTIES ###

    @property
    def argument_parser(self):
        r'''The script's instance of argparse.ArgumentParser.
        '''
        return self._argument_parser

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

    @property
    def program_name(self):
        r'''The name of the script, callable from the command line.
        '''
        name = type(self).__name__[:type(self).__name__.rfind('Script')]
        return stringtools.to_space_delimited_lowercase(name).replace(' ', '-')

    ### PUBLIC METHODS ###

    @staticmethod
    def list_commandline_script_classes():
        r'''Returns a list of all developer script classes.
        '''
        from abjad.tools import abjadbooktools
        from abjad.tools import commandlinetools
        tools_package_paths = []
        tools_package_paths.extend(abjadbooktools.__path__)
        tools_package_paths.extend(commandlinetools.__path__)
        script_classes = []
        for tools_package_path in tools_package_paths:
            generator = documentationtools.yield_all_classes(
                code_root=tools_package_path,
                root_package_name='abjad',
                )
            for commandline_script_class in generator:
                if commandlinetools.CommandlineScript in \
                    inspect.getmro(commandline_script_class) and \
                    not inspect.isabstract(commandline_script_class):
                    script_classes.append(commandline_script_class)
        return list(sorted(script_classes, key=lambda x: x.__name__))

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
