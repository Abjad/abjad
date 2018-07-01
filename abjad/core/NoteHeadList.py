from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.TypedList import TypedList


class NoteHeadList(TypedList):
    r"""
    Note-head list.

    ..  container:: example

        >>> chord = abjad.Chord([0, 1, 4], (1, 4))
        >>> note_heads = abjad.NoteHeadList(
        ...     client=chord,
        ...     items=[11, 10, 9],
        ...     )

        >>> abjad.f(note_heads)
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

    """

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
        import abjad
        self._client = client
        TypedList.__init__(
            self,
            item_class=abjad.NoteHead,
            keep_sorted=True,
            items=items,
            )

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if 'client' in names:
            names.remove('client')
        if 'items' in names:
            names.remove('items')
        if 'keep_sorted' in names:
            names.remove('keep_sorted')
        return FormatSpecification(
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
            if not isinstance(token, abjad.NoteHead):
                token = abjad.NoteHead(written_pitch=token)
                token._client = self.client
            return token
        import abjad
        return coerce_

    ### PUBLIC METHODS ###

    def extend(self, items):
        r"""
        Extends note-heads.

        ..  container:: example

            >>> chord = abjad.Chord("<ef'>")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <ef'>4

            >>> note_heads = []
            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.tweaks.color = 'blue'
            >>> note_heads.append(note_head)
            >>> note_head = abjad.NoteHead("f''")
            >>> note_head.tweaks.color = 'green'
            >>> note_heads.append(note_head)
            >>> chord.note_heads.extend(note_heads)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <
                    ef'
                    \tweak color #blue
                    cs''
                    \tweak color #green
                    f''
                >4

        Returns note-head.
        """
        return super().extend(items)

    def get(self, pitch):
        r"""
        Gets note-head by ``pitch``.

        ..  container:: example

            Gets note-head by pitch name:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> note_head = chord.note_heads.get("e'")
            >>> note_head.tweaks.color = 'red'
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <
                    \tweak color #red
                    e'
                    cs''
                    f''
                >4

        ..  container:: example

            Gets note-head by pitch number:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> note_head = chord.note_heads.get(4)
            >>> note_head.tweaks.color = 'red'
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <
                    \tweak color #red
                    e'
                    cs''
                    f''
                >4

        Raises missing note-head error when chord contains no
        note-head with ``pitch``.

        Raises extra note-head error when chord contains more than
        one note-head with ``pitch``.

        Returns note-head.
        """
        import abjad
        result = []
        pitch = abjad.NamedPitch(pitch)
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
        r"""
        Pops note-head ``i``.

        ..  container:: example

            >>> chord = abjad.Chord("<ef' c'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <ef' c'' f''>4

            >>> chord.note_heads.pop(1)
            NoteHead("c''")

            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <ef' f''>4

        Returns note-head.
        """
        return super().pop(i=i)

    def remove(self, item):
        r"""
        Removes ``item``.

        ..  container:: example

            >>> chord = abjad.Chord("<ef' c'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <ef' c'' f''>4

            >>> note_head = chord.note_heads[1]
            >>> chord.note_heads.remove(note_head)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <ef' f''>4

        """
        return super().remove(item)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Gets client.
        """
        return self._client
