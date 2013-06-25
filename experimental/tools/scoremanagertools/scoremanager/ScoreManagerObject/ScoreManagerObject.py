import abc
import inspect
import os
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.abctools.ContextManager import ContextManager
from experimental.tools.scoremanagertools.scoremanager.ScoreManagerConfiguration \
    import ScoreManagerConfiguration


class ScoreManagerObject(AbjadObject):

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    configuration = ScoreManagerConfiguration()

    cache_file_path = os.path.join(
        configuration.configuration_directory_path, 'cache.py')
    if os.path.exists(cache_file_path):
        cache_file_pointer = file(cache_file_path, 'r')
        cache_lines = cache_file_pointer.read()
        cache_file_pointer.close()
        exec(cache_lines)

    ### CONTEXT MANAGER ###

    class backtracking(ContextManager):
        def __init__(self, client):
            self.client = client
        def __enter__(self):
            self.client._session.push_backtrack()
        def __exit__(self, exg_type, exc_value, trackeback):
            self.client._session.pop_backtrack()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.scoremanager.Session()
        self._io = scoremanagertools.io.IOManager(session=self._session)
        self.backtracking = ScoreManagerObject.backtracking(self)

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Score manager object repr.

        Return string.
        '''
        return '{}()'.format(self._class_name)

    ### PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return

    @property
    def _keyword_argument_names(self):
        result = []
        result.extend(AbjadObject._keyword_argument_names.fget(self))
        result.remove('session')
        return tuple(result)

    @property
    def _space_delimited_lowercase_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            self._class_name)

    @property
    def _spaced_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            self._class_name)

    @property
    def _where(self):
        if self._session.enable_where:
            return inspect.stack()[1]
