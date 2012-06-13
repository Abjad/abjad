#! /usr/bin/env python

from abjad.tools import abctools
from abjad.tools import stringtools
from abc import abstractmethod, abstractproperty
import argparse
import os


class DeveloperScript(abctools.AbjadObject):
    '''Abjad object-oriented model of a developer script:

    ::

        >>> from experimental.abjadbooktools import DeveloperScript

    ::

        >>> script = DeveloperScript()
        >>> script.program_name
        'developer'

    It can be used from the command line:

    ::

        $ ./DeveloperScript.py --help
        usage: developer [-h] [--version]

        A short description.

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit

        A long description.

    ::

        $ ./DeveloperScript.py --version
        developer 1.0

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_argument_parser',)

    ### CLASS INITIALIZER ###

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
        self._setup_argument_parser(parser)

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        if args is None:
            args = self.argument_parser.parse_args()
        else:
            if isinstance(args, str):
                args = args.split()
            elif not isinstance(args, (list, tuple)):
                raise ValueError
            args = self.argument_parser.parse_args(args)
        self._process_args(args)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def argument_parser(self):
        return self._argument_parser

    @property
    def formatted_help(self):
        return self._argument_parser.format_help()

    @property
    def formatted_usage(self):
        return self._argument_parser.format_usage()

    @property
    def formatted_version(self):
        return self._argument_parser.format_version()

    @abstractproperty
    def long_description(self):
        raise NotImplemented

    @property
    def program_name(self):
        name = self._class_name[:self._class_name.rfind('Script')]
        return stringtools.uppercamelcase_to_space_delimited_lowercase(
            name).replace(' ', '-')

    @abstractproperty
    def short_description(self):
        raise NotImplemented

    @abstractproperty
    def version(self):
        raise NotImplemented

    ### PRIVATE METHODS ###

    @abstractmethod
    def _process_args(self, args):
        pass

    @abstractmethod
    def _setup_argument_parser(self):
        pass


if __name__ == '__main__':
    script_name = os.path.basename(__file__).rstrip('.py')
    eval(script_name)()()
