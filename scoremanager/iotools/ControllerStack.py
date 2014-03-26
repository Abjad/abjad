# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class ControllerStack(ContextManager):
    r'''ControllerStack context manager.
    '''

    ### INITIALIZER ###

    def __init__(self, controller):
        self.controller = controller

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters controller stack context manager.

        Returns none.
        '''
        self.controller._session._push_controller(self.controller)

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits controller stack context manager.

        Returns none.
        '''
        self.controller._session._pop_controller()

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}({!r})>'.format(type(self).__name__, self.controller)