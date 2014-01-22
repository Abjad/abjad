# -*- encoding: utf-8 -*-
import os
from abjad.tools.abctools import ContextManager


class TemporaryDirectoryChange(ContextManager):
    r'''A context manager for temporarily changing the current working
    directory.
    '''

    ### INITIALIZER ###

    def __init__(self, directory_path=None):
        if directory_path is not None:
            assert os.path.isdir(directory_path)
        self._directory_path = directory_path

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager and changes to `directory_path`.
        '''
        self._original_directory_path = os.getcwd()
        if self._directory_path is not None:
            os.chdir(self.directory_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager and returns to original working directory.
        '''
        if self._directory_path is not None:
            os.chdir(self._original_directory_path)

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}()>'.format(type(self).__name__)

    ### PUBLIC PROPERTIES ###

    @property
    def directory_path(self):
        r'''Gets temporary directory path of context manager.

        Returns string.
        '''
        return self._directory_path
