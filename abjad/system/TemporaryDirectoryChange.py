import os
import pathlib
from .ContextManager import ContextManager


class TemporaryDirectoryChange(ContextManager):
    """
    A context manager for temporarily changing the current working
    directory.
    """

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
        elif isinstance(directory, pathlib.Path):
            directory = str(directory)
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
        """
        Enters context manager and changes to ``directory``.
        """
        self._original_directory = os.getcwd()
        if self._directory is not None:
            os.chdir(self.directory)
            if self.verbose:
                message = 'Changing directory to {} ...'
                message = message.format(self.directory)
                print(message)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits context manager and returns to original working directory.
        """
        if self._directory is not None:
            os.chdir(self._original_directory)
            if self.verbose:
                message = 'Returning to {} ...'
                message = message.format(self.original_directory)
                print(message)
        self._original_directory = None

    def __repr__(self):
        """
        Gets interpreter representation of context manager.

        Returns string.
        """
        return '<{}()>'.format(type(self).__name__)

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self):
        """
        Gets temporary directory of context manager.

        Returns string.
        """
        return self._directory

    @property
    def original_directory(self):
        """
        Gets original directory of context manager.

        Returns string.
        """
        return self._original_directory

    @property
    def verbose(self):
        """
        Is true if context manager prints verbose messages on entrance and
        exit.

        Returns true or false.
        """
        return self._verbose
