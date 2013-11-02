# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class NoteHeadInventory(TypedList):
    r'''An ordered list of note heads.

    ::

        >>> chord = Chord([0, 1, 4], (1, 4))
        >>> inventory = scoretools.NoteHeadInventory(
        ...     client=chord,
        ...     tokens=[11, 10, 9],
        ...     )

    ::

        >>> inventory
        NoteHeadInventory([NoteHead("a'"), NoteHead("bf'"), NoteHead("b'")], client=Chord("<c' cs' e'>4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        tokens=None,
        client=None,
        ):
        from abjad.tools import scoretools
        self._client = client
        TypedList.__init__(
            self,
            item_class=scoretools.NoteHead,
            keep_sorted=True,
            tokens=tokens,
            )

    ### PRIVATE PROPERTIES ##

    @property
    def _item_callable(self):
        from abjad.tools import scoretools
        def coerce(token):
            note_head = scoretools.NoteHead(
                written_pitch=token,
                )
            note_head._client = self.client
            return note_head
        return coerce

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''The note head inventory's chord client.
        '''
        return self._client
