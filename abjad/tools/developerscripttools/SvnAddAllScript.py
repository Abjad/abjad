# -*- encoding: utf-8 -*-
from abjad.tools import iotools
from abjad.tools.developerscripttools.DirectoryScript import DirectoryScript
import argparse
import os
import subprocess


class SvnAddAllScript(DirectoryScript):
    r'''Run `svn add` on all unversioned files in path:

    ..  shell::
    
        ajv svn add --help

    Return `SvnAddAllScript` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'add'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'svn'

    @property
    def short_description(self):
        return '"svn add" all unversioned files in PATH.'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):
        command = 'svn st {}'.format(args.path)
        process = subprocess.Popen(command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        lines = process.stdout.readlines()
        for line in lines:
            if line.startswith('?'):
                command = 'svn add {}'.format(line.split()[-1])
                iotools.IOManager.spawn_subprocess(command)

    def setup_argument_parser(self, parser):
        parser.add_argument('path',
            default=os.getcwd(),
            nargs='?',
            help='directory tree to be recursed over',
            type=self._validate_path,
            )
