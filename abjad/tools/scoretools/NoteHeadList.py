# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TypedList import TypedList


class NoteHeadList(TypedList):
    r'''Note-head list.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> chord = abjad.Chord([0, 1, 4], (1, 4))
            >>> note_heads = abjad.NoteHeadList(
            ...     client=chord,
            ...     items=[11, 10, 9],
            ...     )

        ::

            >>> f(note_heads)
            abjad.NoteHeadList(
                [
                    abjad.NoteHead(
                        written_pitch=abjad.NamedPitch("a'"),
                        ),
                    abjad.NoteHead(
                        written_pitch=abjad.NamedPitch("bf'"),
                        ),
                    abjad.NoteHead(
                        written_pitch=abjad.NamedPitch("b'"),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Note-heads'

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

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if 'client' in names:
            names.remove('client')
        if 'items' in names:
            names.remove('items')
        if 'keep_sorted' in names:
            names.remove('keep_sorted')
        return systemtools.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_kwargs_names=names,
            )

    def _on_insertion(self, item):
        item._client = self.client

    def _on_removal(self, item):
        item._client = None

    ### PRIVATE PROPERTIES ##

    @property
    def _item_coercer(self):
        def coerce_(token):
            if not isinstance(token, scoretools.NoteHead):
                token = scoretools.NoteHead(
                    written_pitch=token,
                    )
                token._client = self.client
            return token
        from abjad.tools import scoretools
        return coerce_

    ### PUBLIC METHODS ###

    def extend(self, items):
        r'''Extends note-heads.

        ..  container:: example

            ::

                >>> chord = abjad.Chord("<ef'>")
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <ef'>4

            ::

                >>> note_heads = []
                >>> note_head = abjad.NoteHead("cs''")
                >>> note_head.tweak.color = 'blue'
                >>> note_heads.append(note_head)
                >>> note_head = abjad.NoteHead("f''")
                >>> note_head.tweak.color = 'green'
                >>> note_heads.append(note_head)
                >>> chord.note_heads.extend(note_heads)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <
                    ef'
                    \tweak color #blue
                    cs''
                    \tweak color #green
                    f''
                >4

        Returns note-head.
        '''
        superclass = super(NoteHeadList, self)
        return superclass.extend(items)

    def get(self, pitch):
        r'''Gets note-head by `pitch`.

        ..  container:: example

            Gets note-head by pitch name:

            ::

                >>> chord = abjad.Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> note_head = chord.note_heads.get("e'")
                >>> note_head.tweak.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <
                    \tweak color #red
                    e'
                    cs''
                    f''
                >4

        ..  container:: example

            Gets note-head by pitch number:

            ::

                >>> chord = abjad.Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> note_head = chord.note_heads.get(4)
                >>> note_head.tweak.color = 'red'
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <
                    \tweak color #red
                    e'
                    cs''
                    f''
                >4

        Raises missing note-head error when chord contains no
        note-head with `pitch`.

        Raises extra note-head error when chord contains more than
        one note-head with `pitch`.

        Returns note-head.
        '''
        from abjad.tools import pitchtools
        result = []
        pitch = pitchtools.NamedPitch(pitch)
        for note_head in self:
            if note_head.written_pitch == pitch:
                result.append(note_head)
        count = len(result)
        if count == 0:
            message = 'missing note-head.'
            raise ValueError(message)
        elif count == 1:
            note_head = result[0]
            return note_head
        else:
            message = 'extra note-head.'
            raise ValueError(message)

    def pop(self, i=-1):
        r'''Pops note-head `i`.

        ..  container:: example

            ::

                >>> chord = abjad.Chord("<ef' c'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <ef' c'' f''>4

            ::

                >>> chord.note_heads.pop(1)
                NoteHead("c''")

            ::

                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <ef' f''>4

        Returns note-head.
        '''
        superclass = super(NoteHeadList, self)
        return superclass.pop(i=i)

    def remove(self, item):
        r'''Removes `item`.

        ..  container:: example

            ::

                >>> chord = abjad.Chord("<ef' c'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <ef' c'' f''>4

            ::

                >>> note_head = chord.note_heads[1]
                >>> chord.note_heads.remove(note_head)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                <ef' f''>4

        '''
        superclass = super(NoteHeadList, self)
        return superclass.remove(item)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client.
        '''
        return self._client
