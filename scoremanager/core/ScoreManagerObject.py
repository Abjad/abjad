# -*- encoding: utf-8 -*-
import abc
import inspect
import os
from abjad.tools import stringtools
from abjad.tools.abctools.ContextManager import ContextManager


class ScoreManagerObject(object):
    r'''Score manager object.
    '''

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from scoremanager import core
        from scoremanager import iotools
        self._backtrack = iotools.Backtrack(self)
        self._configuration = core.ScoreManagerConfiguration()
        self._session = session or core.Session()
        self._io_manager = iotools.IOManager(self._session)
        self._transcript = self._session.transcript

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    def __ne__(self, expr):
        r'''Is true when types are not the same. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Gets interpreter representation of score manager object.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

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
        if self._session.is_tracking_source_code:
            return inspect.stack()[1]

    ### PRIVATE METHODS ###

    def _exit_io_method(self, source=None):
        from scoremanager import core
        from scoremanager import managers
        if isinstance(source, core.ScoreManager):
            source = 'home'
        elif isinstance(source, managers.ScorePackageManager):
            source = 'score'
        else:
            source = None
        assert source in ('home', 'score', None), repr(source)
        if self._session.is_complete:
            result = True
        elif (self._session.is_backtracking_to_score_manager 
            and not source == 'home'):
            result = True
        elif (self._session.is_backtracking_to_score and 
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_backtracking_locally and 
            not source == 'home' and
            self._session.backtrack_stack):
            result = True
        elif (self._session.is_backtracking_locally and 
            not source == 'home' and
            not self._session.backtrack_stack):
            self._session._is_backtracking_locally = False
            result = True
        elif (self._session.is_navigating_to_score_build_files and
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_navigating_to_score_distribution_files and
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_navigating_to_score_maker_modules and
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_navigating_to_score_materials and
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_navigating_to_score_segments and
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_navigating_to_score_setup and
            not source in ('score', 'home')):
            result = True
        elif (self._session.is_navigating_to_score_stylesheets and
            not source in ('score', 'home')):
            result = True
        else:
            result = False
        return result