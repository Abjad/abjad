# -*- coding: utf-8 -*-
import importlib
import os
import subprocess
import sys
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class PackageGitCommitToken(AbjadValueObject):
    r'''A Python package git commit token.

    ..  container:: example

        ::

            >>> lilypondfiletools.PackageGitCommitToken() # doctest: +SKIP
            PackageGitCommitToken('abjad')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_package_name',
        )

    ### INITIALIZER ###

    def __init__(self, package_name=None):
        self._package_name = package_name

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats package git commit token.

        ..  container:: example

            >>> token = lilypondfiletools.PackageGitCommitToken('abjad')
            >>> print(format(token)) # doctest: +SKIP
            "abjad" revision: 47d96e12550ade33a38036f05430372d2521b8b9

        Return string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PRIVATE METHODS ###

    def _get_git_hash(self):
        module = importlib.import_module(self._package_name)
        path = module.__path__[0]
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        path = os.path.abspath(path)
        with systemtools.TemporaryDirectoryChange(path):
            command = 'git rev-parse HEAD'
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                )
            process.wait()
        if process.returncode:
            return None
        git_hash = process.stdout.read().split()[0]
        if sys.version_info[0] == 3:
            git_hash = git_hash.decode('utf-8')
        return git_hash

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return '"{}" revision: {}'.format(
            self._package_name,
            self._get_git_hash(),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def package_name(self):
        r'''Gets package name of package git commit token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.PackageGitCommitToken('abjad')
                >>> token.package_name
                'abjad'

        Returns string.
        '''
        return self._package_name