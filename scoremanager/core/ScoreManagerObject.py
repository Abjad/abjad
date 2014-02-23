# -*- encoding: utf-8 -*-
import abc
import inspect
import os
from abjad.tools import stringtools
from abjad.tools.abctools.ContextManager import ContextManager


class ScoreManagerObject(object):

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from scoremanager import core
        from scoremanager import iotools
        self._configuration = core.ScoreManagerConfiguration()
        self._session = session or core.Session()
        self.backtracking = iotools.Backtracking(self)

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
        if self._session.enable_where:
            return inspect.stack()[1]

    ### PUBLIC PROPERTIES ###

    @property
    def configuration(self):
        r'''Gets configuration of score manager object.

        Returns score manager configuration.
        '''
        return self._configuration
