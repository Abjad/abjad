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

    __slots__ = (
        '_configuration',
        '_controller_context',
        '_io_manager',
        '_session',
        '_transcript',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from scoremanager import core
        from scoremanager import iotools
        self._configuration = core.ScoreManagerConfiguration()
        self._session = session or core.Session()
        self._io_manager = iotools.IOManager(
            client=self,
            session=self._session,
            )
        self._transcript = self._session.transcript
        self._controller_context = iotools.ControllerContext(self)

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
        return stringtools.to_space_delimited_lowercase(
            type(self).__name__)

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(
            type(self).__name__)

    ### PRIVATE METHODS ###

    def _make_default_hidden_sections(self, menu):
        self._make_go_menu_section(menu)
        self._make_system_menu_section(menu)

    def _make_go_menu_section(self, menu):
        commands = []
        commands.append(('go - back', 'b'))
        commands.append(('go - home', 'h'))
        commands.append(('go - score', 's'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='go',
            )

    def _make_system_menu_section(self, menu):
        commands = []
        commands.append(('system - commands', '?'))
        commands.append(('system - doctest', 'pyd'))
        commands.append(('system - session variables', 'sv'))
        commands.append(('system - LilyPond log', 'll'))
        commands.append(('system - Python', 'pyi'))
        commands.append(('system - pytest', 'pyt'))
        commands.append(('system - quit', 'q'))
        commands.append(('system - shell', '!'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='system', 
            )

    def _should_backtrack(self):
        if self._session.is_quitting:
            return True
        elif self._session.is_backtracking_to_score_manager:
            return True
        elif self._session.is_backtracking_locally:
            self._session._is_backtracking_locally = False
            return True
        elif self._session.is_backtracking_to_score:
            return True
        elif self._session.is_autonavigating_within_score:
            return True
        else:
            return False