# -*- encoding: utf-8 -*-
import argparse
import multiprocessing
import os
import pytest
from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript


class PyTestScript(DirectoryScript):
    r'''Run `py.test` on various Abjad paths:

    ::

        bash$ ajv test -h
        usage: py-test [-h] [--version] [-p] [-x] [-A | -D | -M | -X]

        Run "py.test" on various Abjad paths.

        optional arguments:
          -h, --help          show this help message and exit
          --version           show program's version number and exit
          -p, --parallel      run py.test with multiprocessing
          -x, --exitfirst     stop on first failure
          -A, --all           test all directories, including demos
          -D, --demos         test demos directory
          -M, --mainline      test mainline tools directory
          -X, --experimental  test experimental directory

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
        return 'Run "py.test" on various Abjad paths.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):

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
            help='run py.test with multiprocessing',
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
