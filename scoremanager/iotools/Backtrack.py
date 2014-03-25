# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class Backtrack(ContextManager):
    r'''Backtrack context manager.
    '''

    ### INITIALIZER ###

    def __init__(self, client):
        self.client = client

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters backtrack context manager.

        Returns none.
        '''
        self.client._session._backtrack_stack.append(self)

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits backtrack context manager.

        Returns none.
        '''
        self.client._session._backtrack_stack.pop()