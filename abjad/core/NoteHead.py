import functools
import typing

from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.pitch.NamedPitch import NamedPitch
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager


@functools.total_ordering
class NoteHead(object):
    """
    Note-head.

    ..  container:: example

        >>> note = abjad.Note("cs''")
        >>> abjad.show(note) # doctest: +SKIP

        >>> note.note_head
        NoteHead("cs''")

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Note-heads"

    __slots__ = (
        "_alternative",
        "_client",
        "_is_cautionary",
        "_is_forced",
        "_is_parenthesized",
        "_tweaks",
        "_written_pitch",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        written_pitch=None,
        client=None,
        is_cautionary=None,
        is_forced=None,
        is_parenthesized=None,
        tweaks=None,
    ):
        import abjad

        self._alternative = None
        if client is not None:
            assert isinstance(client, abjad.Leaf)
        self._client = client
        if isinstance(written_pitch, type(self)):
            note_head = written_pitch
            written_pitch = note_head.written_pitch
            is_cautionary = note_head.is_cautionary
            is_forced = note_head.is_forced
            tweaks = note_head.tweaks
        elif written_pitch is None:
            written_pitch = 0
        self.written_pitch = written_pitch
        self.is_cautionary = is_cautionary
        self.is_forced = is_forced
        self.is_parenthesized = is_parenthesized
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        self._tweaks = LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> "NoteHead":
        """
        Copies note-head.

        ..  container:: example

            >>> import copy
            >>> note_head = abjad.NoteHead(13)
            >>> copy.copy(note_head)
            NoteHead("cs''")

        ..  container:: example

            REGRESSION. Note-heads work with new:

            >>> note = abjad.Note("cs''")
            >>> abjad.new(note.note_head)
            NoteHead("cs''")

        """
        arguments = (
            self.written_pitch,
            None,
            self.is_cautionary,
            self.is_forced,
            self.is_parenthesized,
            self.tweaks,
        )
        return type(self)(*arguments)

    def __eq__(self, argument) -> bool:
        """
        Is true when ```argument`` is a note-head with written pitch equal to
        that of this note-head.
        """
        if isinstance(argument, type(self)):
            return self.written_pitch == argument.written_pitch
        return self.written_pitch == argument

    def __format__(self, format_specification="") -> str:
        """
        Formats note-head.
        """
        if format_specification in ("", "lilypond"):
            return self._get_lilypond_format()
        elif format_specification == "storage":
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self) -> int:
        """
        Hashes note-head.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a note-head with written pitch greater
        than that of this note-head.
        """
        if isinstance(argument, type(self)):
            return self.written_pitch < argument.written_pitch
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.written_pitch < argument.written_pitch

    def __repr__(self) -> str:
        """
        Gets interpreter representation of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead(13)
            >>> note_head
            NoteHead("cs''")

        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        """
        Gets string representation of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead(13)
            >>> str(note_head)
            "cs''"

        """
        result = ""
        if self.written_pitch:
            result = str(self.written_pitch)
            if self.is_forced:
                result += "!"
            if self.is_cautionary:
                result += "?"
        return result

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        arguments = [repr(str(self))]
        if self.tweaks:
            arguments.extend(self.tweaks._get_attribute_pairs())
        arguments = ", ".join([str(_) for _ in arguments])
        repr_text = f"{type(self).__name__}({arguments})"
        manager = StorageFormatManager(self)
        names = list(manager.signature_keyword_names)
        if "client" in names:
            names.remove("client")
        if "tweaks" in names:
            names.remove("tweaks")
        return FormatSpecification(
            self, repr_text=repr_text, storage_format_kwargs_names=names
        )

    def _get_format_pieces(self):
        assert self.written_pitch
        result = []
        if self.is_parenthesized:
            result.append(r"\parenthesize")
        if self.tweaks:
            strings = self.tweaks._list_format_contributions(directed=False)
            result.extend(strings)
        written_pitch = self.written_pitch
        if isinstance(written_pitch, NamedPitch):
            written_pitch = written_pitch.simplify()
        kernel = format(written_pitch)
        if self.is_forced:
            kernel += "!"
        if self.is_cautionary:
            kernel += "?"
        result.append(kernel)
        return result

    def _get_lilypond_format(self, duration=None):
        pieces = self._get_format_pieces()
        if duration is not None:
            pieces[-1] = pieces[-1] + duration
        if self.alternative:
            pieces = LilyPondFormatManager.tag(pieces, tag=self.alternative[2])
            pieces_ = self.alternative[0]._get_format_pieces()
            if duration is not None:
                pieces_[-1] = pieces_[-1] + duration
            pieces_ = LilyPondFormatManager.tag(
                pieces_, deactivate=True, tag=self.alternative[1]
            )
            pieces.extend(pieces_)
        result = "\n".join(pieces)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def alternative(self) -> typing.Tuple["NoteHead", str, str]:
        """
        Gets and sets note-head alternative.

        ..  container:: example

            >>> note = abjad.Note("c''4")
            >>> alternative = abjad.new(note.note_head)
            >>> alternative.is_forced = True
            >>> note.note_head.alternative = (alternative, '-PARTS', '+PARTS')
            >>> abjad.show(note) # doctest: +SKIP

            >>> abjad.f(note, strict=50)
            c''4                                              %! +PARTS
            %@% c''!4                                         %! -PARTS

            Survives pitch reassignment:

            >>> note.written_pitch = 'D5'
            >>> abjad.show(note) # doctest: +SKIP

            >>> abjad.f(note, strict=50)
            d''4                                              %! +PARTS
            %@% d''!4                                         %! -PARTS

            Clear with none:

            >>> note.note_head.alternative = None
            >>> abjad.show(note) # doctest: +SKIP

            >>> abjad.f(note, strict=50)
            d''4

        ..  container:: example

            >>> chord = abjad.Chord("<c' d' bf''>4")
            >>> alternative = abjad.new(chord.note_heads[0])
            >>> alternative.is_forced = True
            >>> chord.note_heads[0].alternative = (alternative, '-PARTS', '+PARTS')
            >>> abjad.show(chord) # doctest: +SKIP

            >>> abjad.f(chord, strict=50)
            <
                c'                                            %! +PARTS
            %@% c'!                                           %! -PARTS
                d'
                bf''
            >4

            Suvives pitch reassignment:

            >>> chord.note_heads[0].written_pitch = 'B3'
            >>> abjad.show(chord) # doctest: +SKIP

            >>> abjad.f(chord, strict=50)
            <
                b                                             %! +PARTS
            %@% b!                                            %! -PARTS
                d'
                bf''
            >4

            Clear with none:

            >>> chord.note_heads[0].alternative = None
            >>> abjad.f(chord, strict=50)
            <b d' bf''>4

        """
        return self._alternative

    @alternative.setter
    def alternative(self, argument):
        if argument is not None:
            assert isinstance(argument, tuple), repr(argument)
            assert len(argument) == 3, repr(argument)
            assert isinstance(argument[0], NoteHead), repr(argument)
            assert argument[0].alternative is None, repr(argument)
            assert isinstance(argument[1], str), repr(argument)
            assert isinstance(argument[2], str), repr(argument)
        self._alternative = argument

    @property
    def client(self):
        """
        Gets client of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead(13)
            >>> note_head.client is None
            True

        Returns note, chord or none.
        """
        return self._client

    @property
    def is_cautionary(self) -> bool:
        """
        Gets and sets cautionary accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head.is_cautionary = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c''?4

            >>> note = abjad.Note("cs''")
            >>> note.note_head.is_cautionary = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''?4

        """
        return self._is_cautionary

    @is_cautionary.setter
    def is_cautionary(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._is_cautionary = argument

    @property
    def is_forced(self) -> bool:
        """
        Gets and sets forced accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head.is_forced = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c''!4

            >>> note = abjad.Note("cs''")
            >>> note.note_head.is_forced = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''!4

        """
        return self._is_forced

    @is_forced.setter
    def is_forced(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._is_forced = argument

    @property
    def is_parenthesized(self) -> bool:
        r"""
        Gets and sets forced accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head.is_parenthesized = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                \parenthesize
                c''4

            >>> note = abjad.Note("cs''")
            >>> note.note_head.is_parenthesized = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                \parenthesize
                cs''4

        """
        return self._is_parenthesized

    @is_parenthesized.setter
    def is_parenthesized(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._is_parenthesized = argument

    @property
    def named_pitch(self) -> NamedPitch:
        """
        Gets named pitch.

        ..  container:: example

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.named_pitch
            NamedPitch("cs''")

        """
        return self.written_pitch

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.tweaks is None
            True

            >>> abjad.tweak(note_head).color = 'red'
            >>> note_head.tweaks
            LilyPondTweakManager(('_literal', None), ('color', 'red'))

            >>> abjad.f(note_head)
            \tweak color #red
            cs''

        ..  container:: example

            >>> chord = abjad.Chord([0, 2, 10], (1, 4))

            >>> abjad.tweak(chord.note_heads[0]).color = 'red'
            >>> abjad.tweak(chord.note_heads[0]).thickness = 2

            >>> abjad.tweak(chord.note_heads[1]).color = 'red'
            >>> abjad.tweak(chord.note_heads[1]).thickness = 2

            >>> abjad.tweak(chord.note_heads[2]).color = 'blue'

            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <
                    \tweak color #red
                    \tweak thickness #2
                    c'
                    \tweak color #red
                    \tweak thickness #2
                    d'
                    \tweak color #blue
                    bf'
                >4

            >>> tweaks_1 = chord.note_heads[0].tweaks
            >>> tweaks_2 = chord.note_heads[1].tweaks
            >>> tweaks_3 = chord.note_heads[2].tweaks

            >>> tweaks_1 == tweaks_1
            True

            >>> tweaks_1 == tweaks_2
            True

            >>> tweaks_1 != tweaks_3
            True

            >>> tweaks_2 == tweaks_1
            True

            >>> tweaks_2 == tweaks_2
            True

            >>> tweaks_2 != tweaks_3
            True

            >>> tweaks_3 != tweaks_1
            True

            >>> tweaks_3 != tweaks_2
            True

            >>> tweaks_3 == tweaks_3
            True

        """
        return self._tweaks

    @property
    def written_pitch(self) -> NamedPitch:
        """
        Gets and sets written pitch of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.written_pitch
            NamedPitch("cs''")

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.written_pitch = "d''"
            >>> note_head.written_pitch
            NamedPitch("d''")

        """
        return self._written_pitch

    @written_pitch.setter
    def written_pitch(self, argument):
        written_pitch = NamedPitch(argument)
        self._written_pitch = written_pitch
        if self.alternative is not None:
            self.alternative[0].written_pitch = written_pitch
