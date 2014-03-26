# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class ControllerContext(ContextManager):
    r'''Controller context manager.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        controller=None,
        is_in_confirmation_environment=False,
        on_enter_callbacks=None,
        on_exit_callbacks=None,
        where=None,
        ):
        self.controller = controller
        self.is_in_confirmation_environment = is_in_confirmation_environment
        self.on_enter_callbacks = on_enter_callbacks or ()
        self.on_exit_callbacks = on_exit_callbacks or ()
        self.where = where
        self._session = self.controller._session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters controller stack context manager.

        Returns none.
        '''
        self._session._controller_stack.append(self.controller)
        if self.controller not in self._session.controllers_visited:
            self._session._controllers_visited.append(self.controller)
        self._session._is_in_confirmation_environment = \
            self.is_in_confirmation_environment
        self._session._where = self.where
        self._session._hide_hidden_commands = True
        for on_enter_callback in self.on_enter_callbacks:
            on_enter_callback()

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits controller stack context manager.

        Returns none.
        '''
        self._session._controller_stack.pop()
        self._session._is_in_confirmation_environment = False
        self._session._where = None
        self._session._hide_hidden_commands = True
        for on_exit_callback in self.on_exit_callbacks:
            on_exit_callback()

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}({!r})>'.format(type(self).__name__, self.controller)