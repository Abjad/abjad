import abc
import inspect
import os
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagertools.core.ScoreManagerConfiguration import \
    ScoreManagerConfiguration


class ScoreManagerObject(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __meta__ = abc.ABCMeta
    configuration = ScoreManagerConfiguration()

    cache_file_path = os.path.join(configuration.configuration_directory_path, 'cache.py')
    cache_file_pointer = file(cache_file_path, 'r')
    cache_lines = cache_file_pointer.read()
    cache_file_pointer.close()
    exec(cache_lines)

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.core.Session()
        self._io = scoremanagertools.core.IO(session=self._session)

    ### READ-ONLY PRIVATE PROPERTIES ###

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
        return stringtools.string_to_space_delimited_lowercase(self._class_name)

    @property
    def _spaced_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(self._class_name)
    
    @property
    def _where(self):
        if self._session.enable_where:
            return inspect.stack()[1]
