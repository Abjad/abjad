# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class ControllerStack(ContextManager):
    r'''ControllerStack context manager.
    '''

    ### INITIALIZER ###

    def __init__(self, controller):
        self.controller = controller
        self._session = self.controller._session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters controller stack context manager.

        Returns none.
        '''
        self._session._controller_stack.append(self.controller)
        if self.controller not in self._session.controllers_visited:
            self._session._controllers_visited.append(self.controller)
        self._session._hide_hidden_commands = True

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits controller stack context manager.

        Returns none.
        '''
        self._session._controller_stack.pop()
        self._session._hide_hidden_commands = True

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}({!r})>'.format(type(self).__name__, self.controller)