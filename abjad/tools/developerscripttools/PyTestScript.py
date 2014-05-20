# -*- encoding: utf-8 -*-
import argparse
import multiprocessing
import os
from abjad.tools import systemtools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class PyTestScript(DirectoryScript):
    r'''Runs pytest on various Abjad paths.

    ..  shell::

        ajv test --help

    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        r'''Alias of script.

        Returns ``'test'``.
        '''
        return 'test'

    @property
    def long_description(self):
        r'''Long description of script.

        Returns string or none.
        '''
        return None

    @property
    def scripting_group(self):
        r'''Scripting group of script.

        Returns none.
        '''
        return None

    @property
    def short_description(self):
        r'''Short description of script.

        Returns string.
        '''
        return 'Run "pytest" on various Abjad paths.'

    @property
    def version(self):
        r'''Version of script.

        Returns float.
        '''
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        r'''Processes `args`.

        Returns none.
        '''
        import pytest
        parallel = ''
        if args.parallel:
            parallel = '-n {}'.format(multiprocessing.cpu_count())
        exitfirst = ''
        if args.exitfirst:
           exitfirst = '-x'
        report = ''
        if args.report:
            report = '-r {}'.format(args.report)
        print('TESTING:')
        for path in args.path:
            print('\t{}'.format(path))
        print('')
        path = ' '.join(args.path)
        command = '{} {} {} {}'.format(parallel, exitfirst, report, path)
        return pytest.main(command.split())

    def setup_argument_parser(self, parser):
        r'''Sets up argument `parser`.

        Returns none.
        '''
        from abjad import abjad_configuration
        parser.add_argument('-p', '--parallel',
            action='store_true',
            dest='parallel',
            help='run pytest with multiprocessing',
            )
        parser.add_argument('-r', '--report',
            action='store',
            dest='report',
            help='show extra test summary info as specified by chars ' + \
                '(f)ailed, (E)error, (s)skipped, (x)failed, (X)passed.',
            metavar='chars',
            )
        parser.add_argument('-x', '--exitfirst',
            action='store_true',
            dest='exitfirst',
            help='stop on first failure',
            )
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-A', '--all',
            action='store_const',
            const=[abjad_configuration.abjad_root_directory],
            dest='path',
            help='test all directories, including demos',
            )
        group.add_argument('-D', '--demos',
            action='store_const',
            const=[os.path.join(
                abjad_configuration.abjad_directory, 'demos')],
            dest='path',
            help='test demos directory',
            )
        group.add_argument('-M', '--mainline',
            action='store_const',
            const=[os.path.join(
                abjad_configuration.abjad_directory, 'tools')],
            dest='path',
            help='test mainline tools directory',
            )
        group.add_argument('-X', '--experimental',
            action='store_const',
            const=[abjad_configuration.abjad_experimental_directory],
            dest='path',
            help='test experimental directory',
            )
        parser.set_defaults(path=[
            os.path.join(abjad_configuration.abjad_directory, 'tools'),
            abjad_configuration.abjad_experimental_directory
            ])