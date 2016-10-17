# -*- coding: utf-8 -*-
from __future__ import print_function
import abc
import argparse
import inspect
import os
from abjad.tools import abctools
from abjad.tools import documentationtools
from abjad.tools import stringtools
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


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
        '_config_parser',
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
        self._setup_argument_parser(parser)
        self._config_parser = None

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        r'''Calls developer script.

        Returns none.
        '''
        self._config_parser = self._read_config_files()
        if args is None:
            args = self.argument_parser.parse_args()
        else:
            if isinstance(args, str):
                args = args.split()
            elif not isinstance(args, (list, tuple)):
                raise ValueError
            args = self.argument_parser.parse_args(args)
        self._process_args(args)

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

    @abc.abstractmethod
    def _process_args(self, args):
        raise NotImplementedError

    def _read_config_files(self):
        paths = []
        home_config = pathlib.Path(os.path.expanduser('~/.ajv'))
        if home_config.exists():
            paths.append(home_config)
        path = pathlib.Path.cwd()
        while not path.joinpath('.ajv').exists():
            path = path.parent
            if path.parent == path:
                break
        if path.joinpath('.ajv').exists():
            if path.joinpath('.ajv') not in paths:
                paths.append(path.joinpath('.ajv'))
        paths = [str(_) for _ in paths]
        config_parser = ConfigParser()
        config_parser.read(paths)
        return config_parser

    @abc.abstractmethod
    def _setup_argument_parser(self, parser):
        raise NotImplementedError

    def _validate_path(self, path):
        message = '{!r} is not a valid directory.'
        message = message.format(path)
        error = argparse.ArgumentTypeError(message)
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return os.path.relpath(path)

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
        base_class = commandlinetools.CommandlineScript
        for tools_package_path in tools_package_paths:
            generator = documentationtools.yield_all_classes(
                code_root=tools_package_path,
                root_package_name='abjad',
                )
            for class_ in generator:
                if (
                    issubclass(class_, base_class) and
                    class_ is not base_class and
                    not inspect.isabstract(class_)
                    ):
                    script_classes.append(class_)
        return list(sorted(script_classes, key=lambda x: x.__name__))

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
