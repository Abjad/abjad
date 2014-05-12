# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class Interaction(ContextManager):
    r'''Interation context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controller',
        '_display',
        )

    ### INITIALIZER ###

    def __init__(self, controller=None, display=True):
        self._controller = controller
        self._display = display

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters controller stack context manager.

        Returns none.
        '''
        pass

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits controller stack context manager.

        Returns none.
        '''
        if self.display:
            self.controller._io_manager.display('')
        self.controller._session._hide_next_redraw = True

    ### PUBLIC PROPERTIES ###

    @property
    def controller(self):
        r'''Gets controller of interaction.

        Returns controller.
        '''
        return self._controller

    @property
    def display(self):
        r'''Is true when blank line should display at end of interaction.
        Otherwise false.

        Returns boolean.
        '''
        return self._display