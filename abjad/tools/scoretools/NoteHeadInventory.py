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

        >>> print format(inventory)
        scoretools.NoteHeadInventory([
            scoretools.NoteHead(
                written_pitch=pitchtools.NamedPitch("a'"),
                is_cautionary=False,
                is_forced=False
                ),
            scoretools.NoteHead(
                written_pitch=pitchtools.NamedPitch("bf'"),
                is_cautionary=False,
                is_forced=False
                ),
            scoretools.NoteHead(
                written_pitch=pitchtools.NamedPitch("b'"),
                is_cautionary=False,
                is_forced=False
                ),
            ],
            client=scoretools.Chord(),
            )

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

    ### PRIVATE METHODS ###

    def _on_insertion(self, item):
        item._client = self.client

    def _on_removal(self, item):
        item._client = None

    ### PRIVATE PROPERTIES ##

    @property
    def _item_callable(self):
        from abjad.tools import scoretools
        def coerce(token):
            if not isinstance(token, scoretools.NoteHead):
                token = scoretools.NoteHead(
                    written_pitch=token,
                    )
                token._client = self.client
            return token
        return coerce

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''The note head inventory's chord client.
        '''
        return self._client
