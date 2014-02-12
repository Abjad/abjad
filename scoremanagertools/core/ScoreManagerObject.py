# -*- encoding: utf-8 -*-
import abc
import inspect
import os
from abjad.tools import stringtools
from abjad.tools.abctools.ContextManager import ContextManager
from scoremanagertools.core.ScoreManagerConfiguration \
    import ScoreManagerConfiguration


class ScoreManagerObject(object):

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    configuration = ScoreManagerConfiguration()

    cache_file_path = os.path.join(
        configuration.configuration_directory_path, 'cache.py')
    if os.path.exists(cache_file_path):
        with file(cache_file_path, 'r') as cache_file_pointer:
            cache_lines = cache_file_pointer.read()
        try:
            exec(cache_lines)
        except SyntaxError:
            start_menu_entries = []

    ### CONTEXT MANAGER ###

    class backtracking(ContextManager):
        def __init__(self, client):
            self.client = client
        def __enter__(self):
            self.client.session.push_backtrack()
        def __exit__(self, exg_type, exc_value, trackeback):
            self.client.session.pop_backtrack()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.core.Session()
        self.backtracking = ScoreManagerObject.backtracking(self)

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of score manager object.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return

#    @property
#    def _keyword_argument_names(self):
#        result = []
#        result.extend(AbjadObject._keyword_argument_names.fget(self))
#        result.remove('session')
#        return tuple(result)

    @property
    def _space_delimited_lowercase_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            type(self).__name__)

    @property
    def _spaced_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            type(self).__name__)

    @property
    def _where(self):
        if self.session.enable_where:
            return inspect.stack()[1]

    ### PUBLIC PROPERTIES ###

    @property
    def session(self):
        '''Session of score manager object.

        Returns session.
        '''
        return self._session
