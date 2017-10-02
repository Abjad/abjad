import shutil
import tempfile
from abjad.tools.abctools.ContextManager import ContextManager


class TemporaryDirectory(ContextManager):
    r'''A temporary directory context manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_parent_directory',
        '_temporary_directory',
        )

    ### INITIALIZER ###

    def __init__(self, parent_directory=None):
        self._parent_directory = parent_directory
        self._temporary_directory = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.

        Creates and returns path to a temporary directory.
        '''
        self._temporary_directory = tempfile.mkdtemp(
            dir=self.parent_directory,
            )
        return self._temporary_directory

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager.

        Deletes previously created temporary directory.
        '''
        shutil.rmtree(self._temporary_directory)

    ### PUBLIC PROPERTIES ###

    @property
    def parent_directory(self):
        r'''Gets parent directory.

        Returns string.
        '''
        return self._parent_directory

    @property
    def temporary_directory(self):
        r'''Gets temporary directory.

        Returns string.
        '''
        return self._temporary_directory
