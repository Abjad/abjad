# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Server(AbjadObject):
    r'''Server.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_source',
        )

    ### INITIALIZER ###

    def __init__(self, source=None):
        from abjad.tools import datastructuretools
        self._source = datastructuretools.CyclicPayloadTree(source)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a server with source equal to
        that of this server. Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            if self.source == expr.source:
                return True
        return False

    def __hash__(self):
        r'''Hashes server.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Server, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets source.

        Set to any iterable.

        Returns cyclic tree.
        '''
        return self._source

    ### PUBLIC METHODS ###

    def make_cursor(self, position=None, reverse=False):
        r'''Makes cursor.

        Returns cursor.
        '''
        from abjad.tools import datastructuretools
        if isinstance(position, int):
            position = (position,)
        cursor = datastructuretools.Cursor(
            source=self,
            position=position,
            )
        return cursor