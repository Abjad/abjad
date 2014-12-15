# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class NoteHeadInventory(TypedList):
    r'''An ordered list of note heads.

    ::

        >>> chord = Chord([0, 1, 4], (1, 4))
        >>> inventory = scoretools.NoteHeadInventory(
        ...     client=chord,
        ...     items=[11, 10, 9],
        ...     )

    ::

        >>> print(format(inventory))
        scoretools.NoteHeadInventory(
            [
                scoretools.NoteHead(
                    written_pitch=pitchtools.NamedPitch("a'"),
                    ),
                scoretools.NoteHead(
                    written_pitch=pitchtools.NamedPitch("bf'"),
                    ),
                scoretools.NoteHead(
                    written_pitch=pitchtools.NamedPitch("b'"),
                    ),
                ]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        client=None,
        ):
        from abjad.tools import scoretools
        self._client = client
        TypedList.__init__(
            self,
            item_class=scoretools.NoteHead,
            keep_sorted=True,
            items=items,
            )

    ### PRIVATE METHODS ###

    def _on_insertion(self, item):
        item._client = self.client

    def _on_removal(self, item):
        item._client = None

    ### PRIVATE PROPERTIES ##

    @property
    def _item_coercer(self):
        from abjad.tools import scoretools
        def coerce_(token):
            if not isinstance(token, scoretools.NoteHead):
                token = scoretools.NoteHead(
                    written_pitch=token,
                    )
                token._client = self.client
            return token
        return coerce_

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=(
                self._collection,
                )
            )

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''The note head inventory's chord client.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def get(self, pitch):
        r'''Gets note head in note head inventory by `pitch`.

        ..  container:: example

            **Example 1.** Gets note head by pitch name:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> note_head = chord.note_heads.get("e'")
                >>> note_head.tweak.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                <
                    \tweak #'color #red
                    e'
                    cs''
                    f''
                >4

        ..  container:: example

            **Example 2.** Gets note head by pitch number:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> note_head = chord.note_heads.get(4)
                >>> note_head.tweak.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                <
                    \tweak #'color #red
                    e'
                    cs''
                    f''
                >4

        Raises missing note head error when chord contains no
        note head with `pitch`.

        Raises extra note head error when chord contains more than
        one note head with `pitch`.

        Returns note head.
        '''
        from abjad.tools import pitchtools
        result = []
        pitch = pitchtools.NamedPitch(pitch)
        for note_head in self:
            if note_head.written_pitch == pitch:
                result.append(note_head)
        count = len(result)
        if count == 0:
            message = 'missing note head.'
            raise ValueError(message)
        elif count == 1:
            note_head = result[0]
            return note_head
        else:
            message = 'extra note head.'
            raise ValueError(message)