# -*- encoding: utf-8 -*-
import os
from abjad.tools.abctools import ContextManager


class TemporaryDirectoryChange(ContextManager):
    r'''A context manager for temporarily changing the current working
    directory.
    '''

    ### INITIALIZER ###

    def __init__(self, directory=None):
        if directory is None:
            pass
        elif os.path.isdir(directory):
            pass
        elif os.path.isfile(directory):
            directory = os.path.dirname(directory)
        self._directory = directory

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager and changes to `directory`.
        '''
        self._original_directory = os.getcwd()
        if self._directory is not None:
            os.chdir(self.directory)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager and returns to original working directory.
        '''
        if self._directory is not None:
            os.chdir(self._original_directory)

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}()>'.format(type(self).__name__)

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self):
        r'''Gets temporary directory of context manager.

        Returns string.
        '''
        return self._directory