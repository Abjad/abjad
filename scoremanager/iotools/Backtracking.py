# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class Backtracking(ContextManager):
    r'''Backtracking context manager.
    '''

    ### INITIALIZER ###

    def __init__(self, client):
        self.client = client

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.client._session._push_backtrack()

    def __exit__(self, exg_type, exc_value, trackeback):
        self.client._session._pop_backtrack()
