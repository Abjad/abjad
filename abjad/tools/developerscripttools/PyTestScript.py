# -*- encoding: utf-8 -*-
import argparse
import multiprocessing
import os
from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class PyTestScript(DirectoryScript):
    r'''Run `pytest` on various Abjad paths:

    ..  shell::

        ajv test --help

    Return `PyTestScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'test'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'Run "pytest" on various Abjad paths.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
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

        print 'TESTING:'
        for path in args.path:
            print '\t{}'.format(path)
        print ''

        path = ' '.join(args.path)
        command = '{} {} {} {}'.format(parallel, exitfirst, report, path)

        return pytest.main(command.split())

    def setup_argument_parser(self, parser):

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
            const=[abjad_configuration.abjad_root_directory_path],
            dest='path',
            help='test all directories, including demos',
            )

        group.add_argument('-D', '--demos',
            action='store_const',
            const=[os.path.join(
                abjad_configuration.abjad_directory_path, 'demos')],
            dest='path',
            help='test demos directory',
            )

        group.add_argument('-M', '--mainline',
            action='store_const',
            const=[os.path.join(
                abjad_configuration.abjad_directory_path, 'tools')],
            dest='path',
            help='test mainline tools directory',
            )

        group.add_argument('-X', '--experimental',
            action='store_const',
            const=[abjad_configuration.abjad_experimental_directory_path],
            dest='path',
            help='test experimental directory',
            )

        parser.set_defaults(path=[
            os.path.join(abjad_configuration.abjad_directory_path, 'tools'),
            abjad_configuration.abjad_experimental_directory_path
            ])
