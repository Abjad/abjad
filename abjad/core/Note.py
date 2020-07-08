import typing

from .. import typings
from ..duration import Duration
from ..ly.drums import drums
from ..pitch.pitches import NamedPitch
from ..tags import Tag
from .Leaf import Leaf
from .noteheads import DrumNoteHead, NoteHead


class Note(Leaf):
    """
    Note.

    ..  container:: example

        >>> note = abjad.Note("cs''8.")
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            cs''8.

    ..  container:: example

        REGRESSION. Initialized from other note:

        >>> note = abjad.Note("cs''4", multiplier=(1, 1))
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            cs''4 * 1

        >>> new_note = abjad.Note(note)
        >>> abjad.show(new_note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(new_note)
            cs''4 * 1

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Leaves"

    __slots__ = ("_note_head",)

    ### INITIALIZER ###

    def __init__(
        self, *arguments, multiplier: typings.DurationTyping = None, tag: Tag = None,
    ) -> None:
        assert len(arguments) in (0, 1, 2)
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f"{{ {arguments[0]} }}"
            parsed = self._parse_lilypond_string(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arguments = tuple([parsed[0]])
        written_pitch = None
        is_cautionary = False
        is_forced = False
        is_parenthesized = False
        # if len(arguments) == 1 and isinstance(arguments[0], Leaf):
        if len(arguments) == 1 and hasattr(arguments[0], "written_duration"):
            leaf = arguments[0]
            written_pitch = None
            written_duration = leaf.written_duration
            if multiplier is None:
                multiplier = leaf.multiplier
            if isinstance(leaf, Note) and leaf.note_head is not None:
                written_pitch = leaf.note_head.written_pitch
                is_cautionary = leaf.note_head.is_cautionary
                is_forced = leaf.note_head.is_forced
                is_parenthesized = leaf.note_head.is_parenthesized
            # TODO: move into separate from_chord() constructor:
            elif hasattr(leaf, "written_pitches"):
                written_pitches = [x.written_pitch for x in leaf.note_heads]
                if written_pitches:
                    written_pitch = written_pitches[0]
                    is_cautionary = leaf.note_heads[0].is_cautionary
                    is_forced = leaf.note_heads[0].is_forced
                    is_parenthesized = leaf.note_heads[0].is_parenthesized
        elif len(arguments) == 2:
            written_pitch, written_duration = arguments
        elif len(arguments) == 0:
            written_pitch = NamedPitch("C4")
            written_duration = Duration(1, 4)
        else:
            raise ValueError("can not initialize note from {arguments!r}.")
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if written_pitch is not None:
            if written_pitch not in drums:
                self.note_head = NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
            else:
                assert isinstance(written_pitch, str), repr(written_pitch)
                self.note_head = DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
        else:
            self._note_head = None
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> typing.Tuple:
        """
        Gets new arguments.
        """
        return (self.written_pitch, self.written_duration)

    ### PRIVATE METHODS ###

    def _get_body(self):
        duration = self._get_formatted_duration()
        if self.note_head is not None:
            string = self.note_head._get_lilypond_format(duration=duration)
        else:
            string = duration
        return [string]

    def _get_compact_representation(self):
        return self._get_body()[0]

    ### PUBLIC PROPERTIES ###

    @property
    def note_head(self) -> typing.Optional[NoteHead]:
        """
        Gets and sets note-head.

        .. container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.note_head
            NoteHead("cs''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''8.

            >>> note.note_head = 'D5'
            >>> note.note_head
            NoteHead("d''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                d''8.

        """
        return self._note_head

    @note_head.setter
    def note_head(self, argument):
        if isinstance(argument, type(None)):
            self._note_head = None
        elif isinstance(argument, NoteHead):
            self._note_head = argument
        else:
            note_head = NoteHead(client=self, written_pitch=argument)
            self._note_head = note_head

    @property
    def written_duration(self) -> Duration:
        """
        Gets and sets written duration.

        ..  container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.written_duration
            Duration(3, 16)

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''8.

            >>> note.written_duration = (1, 16)
            >>> note.written_duration
            Duration(1, 16)

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''16

        """
        return super().written_duration

    @written_duration.setter
    def written_duration(self, argument):
        return Leaf.written_duration.fset(self, argument)

    @property
    def written_pitch(self) -> typing.Optional[NamedPitch]:
        """
        Gets and sets written pitch.

        ..  container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.written_pitch
            NamedPitch("cs''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''8.

            >>> note.written_pitch = 'D5'
            >>> note.written_pitch
            NamedPitch("d''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                d''8.

        """
        if self.note_head is not None:
            return self.note_head.written_pitch
        else:
            return None

    @written_pitch.setter
    def written_pitch(self, argument):
        if argument is None:
            if self.note_head is not None:
                self.note_head.written_pitch = None
        else:
            if self.note_head is None:
                self.note_head = NoteHead(self, written_pitch=None)
            else:
                pitch = NamedPitch(argument)
                self.note_head.written_pitch = pitch

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_and_duration(pitch, duration):
        """
        Makes note from ``pitch`` and ``duration``.

        ..  container:: example

            >>> note = abjad.Note.from_pitch_and_duration('C#5', (3, 16))
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                cs''8.

        """
        note = Note(pitch, duration)
        return note
