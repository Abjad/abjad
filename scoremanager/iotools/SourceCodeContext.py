# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class SourceCodeContext(ContextManager):
    r'''Source code context manager.
    '''

    ### INITIALIZER ###

    def __init__(self, client):
        self.client = client
        self._session = self.client._session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters source code context manager.

        Returns none.
        '''
        self._session._where = self.client.where

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits source code context manager.

        Returns none.
        '''
        self._session._where = None

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        Returns string.
        '''
        return '<{}({!r})>'.format(type(self).__name__, self.controller)