# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class SourceCodeContext(ContextManager):
    r'''Source code context manager.
    '''

    ### INITIALIZER ###

    def __init__(self, menu):
        self.menu = menu
        self._session = self.menu._session

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters source code context manager.

        Returns none.
        '''
        self._session._where = self.menu._client_source_code_location

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