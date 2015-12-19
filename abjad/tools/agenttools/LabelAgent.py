# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools.topleveltools.iterate import iterate


class LabelAgent(abctools.AbjadObject):
    r'''A wrapper around the Abjad label methods.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> label(staff)
            LabelAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        prototype = (
            scoretools.Component, 
            selectiontools.Selection,
            spannertools.Spanner, 
            type(None),
            )
        assert isinstance(client, prototype), repr(client)
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of inspection agent.

        Returns component, selection, spanner or none.
        '''
        return self._client

    ### PUBLIC METHODS ###