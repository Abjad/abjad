# -*- encoding: utf-8 -*-
import os
from abjad.tools.abctools import ContextManager


class TemporaryDirectoryChange(ContextManager):
    r'''A context manager for temporarily changing the current working
    directory.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_directory',
        '_original_directory',
        '_verbose',
        )

    ### INITIALIZER ###

    def __init__(self, directory=None, verbose=None):
        if directory is None:
            pass
        elif os.path.isdir(directory):
            pass
        elif os.path.isfile(directory):
            directory = os.path.dirname(directory)
        self._directory = directory
        self._original_directory = None
        if verbose is not None:
            verbose = bool(verbose)
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager and changes to `directory`.
        '''
        self._original_directory = os.getcwd()
        if self._directory is not None:
            os.chdir(self.directory)
            if self.verbose:
                print('Changing directory to {}.'.format(self.directory))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager and returns to original working directory.
        '''
        if self._directory is not None:
            os.chdir(self._original_directory)
            if self.verbose:
                print('Returning to {}.'.format(self.original_directory))
        self._original_directory = None

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

    @property
    def original_directory(self):
        r'''Gets original directory of context manager.

        Returns string.
        '''
        return self._original_directory

    @property
    def verbose(self):
        r'''Is true if context manager prints verbose messages on entrance and
        exit. Otherwise false.

        Returns boolean.
        '''
        return self._verbose