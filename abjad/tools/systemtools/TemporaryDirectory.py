# -*- coding: utf-8 -*-
import shutil
import tempfile
from abjad.tools.abctools.ContextManager import ContextManager


class TemporaryDirectory(ContextManager):
    r'''A temporary directory context manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_parent_directory_path',
        '_temporary_directory_path',
        )

    ### INITIALIZER ###

    def __init__(self, parent_directory_path=None):
        self._parent_directory_path = parent_directory_path
        self._temporary_directory_path = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.

        Creates and returns path to a temporary directory.
        '''
        self._temporary_directory_path = tempfile.mkdtemp(
            dir=self.parent_directory_path,
            )
        return self._temporary_directory_path

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager.

        Deletes previously created temporary directory.
        '''
        shutil.rmtree(self._temporary_directory_path)

    ### PUBLIC PROPERTIES ###

    @property
    def parent_directory_path(self):
        r'''Gets parent directory path.

        Returns string.
        '''
        return self._parent_directory_path

    @property
    def temporary_directory_path(self):
        r'''Gets temporary directory path.

        Returns string.
        '''
        return self._temporary_directory_path
