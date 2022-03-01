import collections
import dataclasses
import functools
import math
import typing

import quicktions

from . import bundle as _bundle
from . import duration as _duration
from . import enumerate as _enumerate
from . import enums as _enums
from . import markups as _markups
from . import math as _math
from . import overrides as _overrides
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import ratio as _ratio
from . import sequence as _sequence
from . import string as _string
from . import typings as _typings


@dataclasses.dataclass(slots=True)
class Arpeggio:
    r"""
    Arpeggio.

    ..  container:: example

        Without direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio()
        >>> abjad.attach(arpeggio, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' e' g' c''>4
                \arpeggio
            }

    ..  container:: example

        With direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio(direction=abjad.Down)
        >>> abjad.attach(arpeggio, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \arpeggioArrowDown
                <c' e' g' c''>4
                \arpeggio
            }

    ..  container:: example

        Tweaks:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio()
        >>> abjad.tweak(arpeggio).color = "#blue"
        >>> abjad.attach(arpeggio, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' e' g' c''>4
                - \tweak color #blue
                \arpeggio
            }

    """

    direction: int | _enums.VerticalAlignment | None = None
    tweaks: _overrides.TweakInterface | None = None
    _annotation: typing.Any = dataclasses.field(default=None, init=False, repr=False)

    _is_dataclass = True

    def __post_init__(self):
        self._annotation = None
        self.direction = _string.to_tridirectional_ordinal_constant(self.direction)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        return r"\arpeggio"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(r"\arpeggio")
        if self.direction in (_enums.Up, _enums.Down):
            if self.direction is _enums.Up:
                command = r"\arpeggioArrowUp"
            else:
                command = r"\arpeggioArrowDown"
            bundle.before.commands.append(command)
        return bundle


@dataclasses.dataclass(slots=True)
class Articulation:
    r"""
    Articulation.

    ..  container:: example

        Initializes from string:

        >>> abjad.Articulation("staccato")
        Articulation(name='staccato', direction=None, tweaks=None)

        >>> abjad.Articulation(".")
        Articulation(name='.', direction=None, tweaks=None)

        With direction:

        >>> abjad.Articulation("staccato", direction=abjad.Up)
        Articulation(name='staccato', direction=Up, tweaks=None)

    ..  container:: example

        New:

        >>> import dataclasses
        >>> dataclasses.replace(abjad.Articulation("."))
        Articulation(name='.', direction=None, tweaks=None)

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> articulation = abjad.Articulation("marcato")
        >>> abjad.tweak(articulation).color = "#blue"
        >>> abjad.attach(articulation, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            - \marcato

    """

    name: str
    direction: int | _enums.VerticalAlignment | None = None
    tweaks: _overrides.TweakInterface | None = None

    _is_dataclass = True

    _shortcut_to_word = {
        "^": "marcato",
        "+": "stopped",
        "-": "tenuto",
        "|": "staccatissimo",
        ">": "accent",
        ".": "staccato",
        "_": "portato",
    }

    def __post_init__(self):
        assert isinstance(self.name, str), repr(self.name)
        self.direction = _string.to_tridirectional_ordinal_constant(self.direction)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    # TODO: eventually remove
    def __str__(self) -> str:
        """
        Gets string representation of articulation.
        """
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = "-"
            else:
                direction_ = _string.to_tridirectional_lilypond_symbol(self.direction)
                assert isinstance(direction_, str), repr(direction)
                direction = direction_
            return rf"{direction} \{string}"
        else:
            return ""

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class BarLine:
    r"""
    Bar line.

    ..  container:: example

        Final bar line:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> bar_line = abjad.BarLine("|.")
        >>> abjad.attach(bar_line, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> bar_line
        BarLine(abbreviation='|.', format_slot='after')

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \bar "|."
            }

    ..  container:: example

        Specify repeat bars like this:

        >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.BarLine(".|:"), staff[3])
        >>> abjad.attach(abjad.BarLine(":|."), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \bar ".|:"
                g'4
                a'4
                b'4
                c''4
                \bar ":|."
            }

        This allows you to bypass LilyPond's ``\volta`` command.

    """

    abbreviation: str = "|"
    format_slot: str = "after"

    _is_dataclass = True

    _context = "Score"

    # scraped from LilyPond docs because LilyPond fails to error
    # on unrecognized string
    _known_abbreviations = (
        "",
        "|",
        ".",
        "||",
        ".|",
        "..",
        "|.|",
        "|.",
        ";",
        "!",
        ".|:",
        ":..:",
        ":|.|:",
        ":|.:",
        ":.|.:",
        "[|:",
        ":|][|:",
        ":|]",
        ":|.",
        "'",
    )

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return rf'\bar "{self.abbreviation}"'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.append(self._get_lilypond_format())
        return bundle

    @property
    def context(self) -> str:
        r"""
        Gets (historically conventional) context.

        ..  container:: example

            >>> bar_line = abjad.BarLine('|.')
            >>> bar_line.context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context


@dataclasses.dataclass(slots=True)
class BeamCount:
    r"""
    LilyPond ``\setLeftBeamCount``, ``\setRightBeamCount`` command.

    ..  container:: example

        >>> abjad.BeamCount()
        BeamCount(left=0, right=0)

    """

    left: int = 0
    right: int = 0

    _is_dataclass = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = rf"\set stemLeftBeamCount = {self.left}"
        bundle.before.commands.append(string)
        string = rf"\set stemRightBeamCount = {self.right}"
        bundle.before.commands.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class BendAfter:
    r"""
    Fall or doit.

    ..  container:: example

        A fall:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(-4)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \bendAfter #'-4

    ..  container:: example

        A doit:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(2)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \bendAfter #'2

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> bend_after = abjad.BendAfter(-4)
        >>> abjad.tweak(bend_after).color = "#blue"
        >>> abjad.attach(bend_after, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                - \bendAfter #'-4
                d'4
                e'4
                f'4
            }

    """

    bend_amount: _typings.Number = -4
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _format_slot = "after"
    _is_dataclass = True
    _time_orientation = _enums.Right

    # TODO: remove
    def __str__(self) -> str:
        r"""
        Gets string representation of bend after.

        ..  container:: example

            >>> str(abjad.BendAfter())
            "- \\bendAfter #'-4"

        """
        return rf"- \bendAfter #'{self.bend_amount}"

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class BreathMark:
    r"""
    Breath mark.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> breath_mark = abjad.BreathMark()
        >>> abjad.attach(breath_mark, note)
        >>> staff = abjad.Staff([note])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \breathe
            }

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.beam(staff[:4])
        >>> abjad.beam(staff[4:])
        >>> abjad.attach(abjad.BreathMark(), staff[3])
        >>> abjad.attach(abjad.BreathMark(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
                \breathe
                g'8
                [
                a'8
                b'8
                c''8
                ]
                \breathe
            }

    ..  container:: example

        REGRESSION. Abjad parses LilyPond's ``\breathe`` command correctly:

        >>> staff = abjad.Staff(r"c'4 d' e' f' \breathe")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \breathe
            }

    ..  container:: example

        Works with tweaks:

        >>> note = abjad.Note("c'4")
        >>> breath = abjad.BreathMark()
        >>> abjad.tweak(breath).color = "#blue"
        >>> abjad.attach(breath, note)
        >>> staff = abjad.Staff([note])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \tweak color #blue
                \breathe
            }

    """

    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _format_slot = "after"

    _is_dataclass = True

    _time_orientation = _enums.Right

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        return r"\breathe"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.after.articulations.extend(tweaks)
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class StaffPosition:
    """
    Staff position.

    ..  container:: example

        Initializes staff position at middle line of staff:

        >>> abjad.StaffPosition(0)
        StaffPosition(number=0)

    ..  container:: example

        Initializes staff position one space below middle line of staff:

        >>> abjad.StaffPosition(-1)
        StaffPosition(number=-1)

    ..  container:: example

        Initializes staff position one line below middle line of staff:

        >>> abjad.StaffPosition(-2)
        StaffPosition(number=-2)

    ..  container:: example

        Equality-testing:

        >>> staff_position_1 = abjad.StaffPosition(-2)
        >>> staff_position_2 = abjad.StaffPosition(-2)
        >>> staff_position_3 = abjad.StaffPosition(0)

        >>> staff_position_1 == staff_position_1
        True
        >>> staff_position_1 == staff_position_2
        True
        >>> staff_position_1 == staff_position_3
        False

        >>> staff_position_2 == staff_position_1
        True
        >>> staff_position_2 == staff_position_2
        True
        >>> staff_position_2 == staff_position_3
        False

        >>> staff_position_3 == staff_position_1
        False
        >>> staff_position_3 == staff_position_2
        False
        >>> staff_position_3 == staff_position_3
        True

    ..  container:: example

        Less-than:

        >>> staff_position_1 = abjad.StaffPosition(-2)
        >>> staff_position_2 = abjad.StaffPosition(-2)
        >>> staff_position_3 = abjad.StaffPosition(0)

        >>> staff_position_1 < staff_position_1
        False
        >>> staff_position_1 < staff_position_2
        False
        >>> staff_position_1 < staff_position_3
        True

        >>> staff_position_2 < staff_position_1
        False
        >>> staff_position_2 < staff_position_2
        False
        >>> staff_position_2 < staff_position_3
        True

        >>> staff_position_3 < staff_position_1
        False
        >>> staff_position_3 < staff_position_2
        False
        >>> staff_position_3 < staff_position_3
        False

    """

    number: float | int = 0

    def __post_init__(self):
        assert isinstance(self.number, (int, float)), repr(self.number)

    @staticmethod
    def from_pitch_and_clef(pitch, clef) -> "StaffPosition":
        r"""
        Changes named pitch to staff position.

        ..  container:: example

            Changes C#5 to absolute staff position:

            >>> clef = abjad.Clef("alto")
            >>> abjad.StaffPosition.from_pitch_and_clef('C#5', clef)
            StaffPosition(number=7)

            >>> clef = abjad.Clef("treble")
            >>> abjad.StaffPosition.from_pitch_and_clef('C#5', clef)
            StaffPosition(number=1)

            >>> clef = abjad.Clef("bass")
            >>> abjad.StaffPosition.from_pitch_and_clef('C#5', clef)
            StaffPosition(number=13)

        ..  container:: example

            Marks up absolute staff position of many pitches:

            >>> string = "g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''"
            >>> staff = abjad.Staff(string)
            >>> clef = abjad.Clef("alto")
            >>> for note in staff:
            ...     staff_position = abjad.StaffPosition.from_pitch_and_clef(
            ...         note.written_pitch,
            ...         clef,
            ...     )
            ...     markup = abjad.Markup(rf"\markup {staff_position.number}")
            ...     abjad.attach(markup, note)
            ...
            >>> abjad.override(staff).TextScript.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = 5
                }
                {
                    g16
                    - \markup -3
                    a16
                    - \markup -2
                    b16
                    - \markup -1
                    c'16
                    - \markup 0
                    d'16
                    - \markup 1
                    e'16
                    - \markup 2
                    f'16
                    - \markup 3
                    g'16
                    - \markup 4
                    a'16
                    - \markup 5
                    b'16
                    - \markup 6
                    c''16
                    - \markup 7
                    d''16
                    - \markup 8
                    e''16
                    - \markup 9
                    f''16
                    - \markup 10
                    g''16
                    - \markup 11
                    a''16
                    - \markup 12
                }

        ..  container:: example

            Marks up bass staff position of many pitches:

            >>> string = "g,16 a, b, c d e f g a b c' d' e' f' g' a'"
            >>> staff = abjad.Staff(string)
            >>> clef = abjad.Clef("bass")
            >>> for note in staff:
            ...     staff_position = abjad.StaffPosition.from_pitch_and_clef(
            ...         note.written_pitch,
            ...         clef,
            ...     )
            ...     markup = abjad.Markup(rf"\markup {staff_position.number}")
            ...     abjad.attach(markup, note)
            ...
            >>> abjad.attach(abjad.Clef("bass"), staff[0])
            >>> abjad.override(staff).TextScript.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = 5
                }
                {
                    \clef "bass"
                    g,16
                    - \markup -4
                    a,16
                    - \markup -3
                    b,16
                    - \markup -2
                    c16
                    - \markup -1
                    d16
                    - \markup 0
                    e16
                    - \markup 1
                    f16
                    - \markup 2
                    g16
                    - \markup 3
                    a16
                    - \markup 4
                    b16
                    - \markup 5
                    c'16
                    - \markup 6
                    d'16
                    - \markup 7
                    e'16
                    - \markup 8
                    f'16
                    - \markup 9
                    g'16
                    - \markup 10
                    a'16
                    - \markup 11
                }

        """
        assert isinstance(clef, Clef), repr(clef)
        pitch = _pitch.NamedPitch(pitch)
        staff_position_number = pitch._get_diatonic_pitch_number()
        staff_position_number += clef.middle_c_position.number
        staff_position = StaffPosition(staff_position_number)
        return staff_position

    def to_pitch(self, clef):
        """
        Makes named pitch from staff position and ``clef``.

        ..  container:: example

            Treble clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     clef = abjad.Clef("treble")
            ...     pitch = staff_position.to_pitch(clef)
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(number=-6)    c'
            StaffPosition(number=-5)    d'
            StaffPosition(number=-4)    e'
            StaffPosition(number=-3)    f'
            StaffPosition(number=-2)    g'
            StaffPosition(number=-1)    a'
            StaffPosition(number=0)    b'
            StaffPosition(number=1)    c''
            StaffPosition(number=2)    d''
            StaffPosition(number=3)    e''
            StaffPosition(number=4)    f''
            StaffPosition(number=5)    g''

        ..  container:: example

            Bass clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     clef = abjad.Clef("bass")
            ...     pitch = staff_position.to_pitch(clef)
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(number=-6)    e,
            StaffPosition(number=-5)    f,
            StaffPosition(number=-4)    g,
            StaffPosition(number=-3)    a,
            StaffPosition(number=-2)    b,
            StaffPosition(number=-1)    c
            StaffPosition(number=0)    d
            StaffPosition(number=1)    e
            StaffPosition(number=2)    f
            StaffPosition(number=3)    g
            StaffPosition(number=4)    a
            StaffPosition(number=5)    b

        ..  container:: example

            Alto clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     clef = abjad.Clef("alto")
            ...     pitch = staff_position.to_pitch(clef)
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(number=-6)    d
            StaffPosition(number=-5)    e
            StaffPosition(number=-4)    f
            StaffPosition(number=-3)    g
            StaffPosition(number=-2)    a
            StaffPosition(number=-1)    b
            StaffPosition(number=0)    c'
            StaffPosition(number=1)    d'
            StaffPosition(number=2)    e'
            StaffPosition(number=3)    f'
            StaffPosition(number=4)    g'
            StaffPosition(number=5)    a'

        ..  container:: example

            Percussion clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     clef = abjad.Clef("percussion")
            ...     pitch = staff_position.to_pitch(clef)
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(number=-6)    d
            StaffPosition(number=-5)    e
            StaffPosition(number=-4)    f
            StaffPosition(number=-3)    g
            StaffPosition(number=-2)    a
            StaffPosition(number=-1)    b
            StaffPosition(number=0)    c'
            StaffPosition(number=1)    d'
            StaffPosition(number=2)    e'
            StaffPosition(number=3)    f'
            StaffPosition(number=4)    g'
            StaffPosition(number=5)    a'

        Returns new named pitch.
        """
        assert isinstance(clef, Clef), repr(clef)
        offset_staff_position_number = self.number
        offset_staff_position_number -= clef.middle_c_position.number
        offset_staff_position = StaffPosition(offset_staff_position_number)
        octave_number = offset_staff_position.number // 7 + 4
        diatonic_pc_number = offset_staff_position.number % 7
        pitch_class_number = _pitch._diatonic_pc_number_to_pitch_class_number[
            diatonic_pc_number
        ]
        pitch_number = 12 * (octave_number - 4)
        pitch_number += pitch_class_number
        named_pitch = _pitch.NamedPitch(pitch_number)
        return named_pitch


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Clef:
    r"""
    Clef.

    ..  container:: example

        Some available clefs:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> clef = abjad.Clef("treble")
        >>> abjad.attach(clef, staff[0])
        >>> clef = abjad.Clef("alto")
        >>> abjad.attach(clef, staff[1])
        >>> clef = abjad.Clef("bass")
        >>> abjad.attach(clef, staff[2])
        >>> clef = abjad.Clef("treble^8")
        >>> abjad.attach(clef, staff[3])
        >>> clef = abjad.Clef("bass_8")
        >>> abjad.attach(clef, staff[4])
        >>> clef = abjad.Clef("tenor")
        >>> abjad.attach(clef, staff[5])
        >>> clef = abjad.Clef("bass^15")
        >>> abjad.attach(clef, staff[6])
        >>> clef = abjad.Clef("percussion")
        >>> abjad.attach(clef, staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                c'8
                \clef "alto"
                d'8
                \clef "bass"
                e'8
                \clef "treble^8"
                f'8
                \clef "bass_8"
                g'8
                \clef "tenor"
                a'8
                \clef "bass^15"
                b'8
                \clef "percussion"
                c''8
            }

    ..  container:: example

        Clefs can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(
        ...     abjad.Clef("treble"), staff[0], tag=abjad.Tag("+PARTS")
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            %! +PARTS
            \clef "treble"
            c'4
            d'4
            e'4
            f'4
        }

    ..  container:: example

        LilyPond can not handle simultaneous clefs:

        >>> voice_1 = abjad.Voice("e'8 g' f' a' g' b'")
        >>> abjad.attach(abjad.Clef("treble"), voice_1[0], context="Voice")
        >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
        >>> abjad.attach(literal, voice_1)
        >>> voice_1.consists_commands.append("Clef_engraver")
        >>> voice_2 = abjad.Voice("c'4. c,8 b,, a,,")
        >>> abjad.attach(abjad.Clef("treble"), voice_2[0], context="Voice")
        >>> abjad.attach(abjad.Clef("bass"), voice_2[1], context="Voice")
        >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
        >>> abjad.attach(literal, voice_2)
        >>> voice_2.consists_commands.append("Clef_engraver")
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
        >>> staff.remove_commands.append("Clef_engraver")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \remove Clef_engraver
            }
            <<
                \new Voice
                \with
                {
                    \consists Clef_engraver
                }
                {
                    \voiceOne
                    \clef "treble"
                    e'8
                    g'8
                    f'8
                    a'8
                    g'8
                    b'8
                }
                \new Voice
                \with
                {
                    \consists Clef_engraver
                }
                {
                    \voiceTwo
                    \clef "treble"
                    c'4.
                    \clef "bass"
                    c,8
                    b,,8
                    a,,8
                }
            >>

        But Abjad components work fine:

        >>> for leaf in abjad.select.leaves(voice_1):
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("e'8"), Clef(name='treble', hide=False))
        (Note("g'8"), Clef(name='treble', hide=False))
        (Note("f'8"), Clef(name='treble', hide=False))
        (Note("a'8"), Clef(name='treble', hide=False))
        (Note("g'8"), Clef(name='treble', hide=False))
        (Note("b'8"), Clef(name='treble', hide=False))

        >>> for leaf in abjad.select.leaves(voice_2):
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("c'4."), Clef(name='treble', hide=False))
        (Note('c,8'), Clef(name='bass', hide=False))
        (Note('b,,8'), Clef(name='bass', hide=False))
        (Note('a,,8'), Clef(name='bass', hide=False))

    ..  container:: example

        Middle-C position:

        >>> abjad.Clef("treble").middle_c_position
        StaffPosition(number=-6)

        >>> abjad.Clef("alto").middle_c_position
        StaffPosition(number=0)


    ..  container:: example

        Set ``hide=True`` when clef should not appear in output (but should still
        determine effective clef).

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef("treble"), staff[0])
            >>> abjad.attach(abjad.Clef("alto", hide=True), staff[2])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                c'4
                d'4
                e'4
                f'4
            }

            >>> for leaf in abjad.iterate.leaves(staff):
            ...     leaf, abjad.get.effective(leaf, abjad.Clef)
            ...
            (Note("c'4"), Clef(name='treble', hide=False))
            (Note("d'4"), Clef(name='treble', hide=False))
            (Note("e'4"), Clef(name='alto', hide=True))
            (Note("f'4"), Clef(name='alto', hide=True))

    """

    name: str = "treble"
    hide: bool = False
    middle_c_position: StaffPosition = dataclasses.field(init=False, repr=False)

    _is_dataclass = True

    _clef_name_to_middle_c_position = {
        "treble": -6,
        "alto": 0,
        "varC": 0,
        "tenor": 2,
        "tenorvarC": 2,
        "bass": 6,
        "french": -8,
        "soprano": -4,
        "mezzosoprano": -2,
        "baritone": 4,
        "varbaritone": 4,
        "percussion": 0,
        "tab": 0,
    }

    _format_slot = "opening"

    context = "Staff"
    persistent = True
    redraw = True

    _to_width = {
        "alto": 2.75,
        "varC": 2.75,
        "bass": 2.75,
        "percussion": 2.5,
        "tenor": 2.75,
        "tenorvarC": 2.75,
        "treble": 2.5,
    }

    def __post_init__(self):
        assert isinstance(self.name, str), repr(self.name)
        middle_c_position = self._calculate_middle_c_position(self.name)
        middle_c_position = StaffPosition(middle_c_position)
        self.middle_c_position = middle_c_position

    def _calculate_middle_c_position(self, clef_name):
        alteration = 0
        if "_" in self.name:
            base_name, part, suffix = clef_name.partition("_")
            if suffix == "8":
                alteration = 7
            elif suffix == "15":
                alteration = 13
            else:
                raise Exception(f"bad clef alteration suffix: {suffix!r}.")
        elif "^" in self.name:
            base_name, part, suffix = clef_name.partition("^")
            if suffix == "8":
                alteration = -7
            elif suffix == "15":
                alteration = -13
            else:
                raise Exception(f"bad clef alteration suffix: {suffix!r}.")
        else:
            base_name = clef_name
        return self._clef_name_to_middle_c_position[base_name] + alteration

    def _clef_name_to_staff_position_zero(self, clef_name):
        return {
            "treble": _pitch.NamedPitch("B4"),
            "alto": _pitch.NamedPitch("C4"),
            "varC": _pitch.NamedPitch("C4"),
            "tenor": _pitch.NamedPitch("A3"),
            "tenorvarC": _pitch.NamedPitch("A3"),
            "bass": _pitch.NamedPitch("D3"),
            "french": _pitch.NamedPitch("D5"),
            "soprano": _pitch.NamedPitch("G4"),
            "mezzosoprano": _pitch.NamedPitch("E4"),
            "baritone": _pitch.NamedPitch("F3"),
            "varbaritone": _pitch.NamedPitch("F3"),
            "percussion": None,
            "tab": None,
        }[clef_name]

    def _get_lilypond_format(self):
        return rf'\clef "{self.name}"'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if not self.hide:
            bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    @classmethod
    def from_pitches(class_, pitches) -> "Clef":
        """
        Makes clef from ``pitches``.

        ..  container:: example

            >>> maker = abjad.NoteMaker()
            >>> notes = maker(list(range(-12, -6)), [(1, 4)])
            >>> staff = abjad.Staff(notes)
            >>> pitches = abjad.iterate.pitches(staff)
            >>> abjad.Clef.from_pitches(pitches)
            Clef(name='bass', hide=False)

            Choses between treble and bass based on minimal number of ledger lines.

        """
        diatonic_pitch_numbers = [
            pitch._get_diatonic_pitch_number() for pitch in pitches
        ]
        max_diatonic_pitch_number = max(diatonic_pitch_numbers)
        min_diatonic_pitch_number = min(diatonic_pitch_numbers)
        lowest_treble_line_pitch = _pitch.NamedPitch("E4")
        lowest_treble_line_diatonic_pitch_number = (
            lowest_treble_line_pitch._get_diatonic_pitch_number()
        )
        candidate_steps_below_treble = (
            lowest_treble_line_diatonic_pitch_number - min_diatonic_pitch_number
        )
        highest_bass_line_pitch = _pitch.NamedPitch("A3")
        highest_bass_line_diatonic_pitch_number = (
            highest_bass_line_pitch._get_diatonic_pitch_number()
        )
        candidate_steps_above_bass = (
            max_diatonic_pitch_number - highest_bass_line_diatonic_pitch_number
        )
        if candidate_steps_above_bass < candidate_steps_below_treble:
            return class_("bass")
        else:
            return class_("treble")


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class ColorFingering:
    r"""
    Color fingering.

    ..  container:: example

        First color fingering:

        >>> fingering = abjad.ColorFingering(1)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }

    ..  container:: example

        Second color fingering:

        >>> fingering = abjad.ColorFingering(2)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }

    Color fingerings indicate alternate woodwind fingerings by amount of pitch of timbre
    deviation.

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> fingering = abjad.ColorFingering(1)
        >>> abjad.tweak(fingering).color = "#blue"
        >>> abjad.attach(fingering, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                d'4
                e'4
                f'4
            }

    """

    number: int
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    _format_slot = "after"

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        return self.markup._get_lilypond_format()

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.markup.extend(tweaks)
        markup = self.markup
        markup = dataclasses.replace(markup, direction=_enums.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.after.markup.extend(markup_format_pieces)
        return bundle

    @property
    def markup(self) -> typing.Optional[_markups.Markup]:
        r"""
        Gets markup of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> string = abjad.lilypond(fingering.markup)
            >>> print(string)
            \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }

        ..  container:: example

            Second color fingering:

            >>> fingering = abjad.ColorFingering(2)
            >>> string = abjad.lilypond(fingering.markup)
            >>> print(string)
            \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }

        """
        if self.number is None:
            return None
        string = rf"\override #'(circle-padding . 0.25) \circle \finger {self.number}"
        string = rf"\markup {{ {string} }}"
        markup = _markups.Markup(string)
        return markup


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Fermata:
    r"""
    Fermata.

    ..  container:: example

        A short fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata(command='shortfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \shortfermata
                }
            >>

    ..  container:: example

        A fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata()
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \fermata
                }
            >>

    ..  container:: example

        A long fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata('longfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \longfermata
                }
            >>

    ..  container:: example

        A very long fermata:

        >>> score = abjad.Score([abjad.Staff([abjad.Note("c'4")])])
        >>> fermata = abjad.Fermata('verylongfermata')
        >>> abjad.attach(fermata, score[0][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    \verylongfermata
                }
            >>

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> fermata = abjad.Fermata()
        >>> abjad.tweak(fermata).color = "#blue"
        >>> abjad.attach(fermata, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \fermata

    """

    command: str = "fermata"
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    _allowable_commands = (
        "fermata",
        "longfermata",
        "shortfermata",
        "verylongfermata",
    )

    context = "Score"

    _format_slot = "after"

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def __str__(self) -> str:
        r"""
        Gets string representation of fermata.

        ..  container:: example

            Fermata:

            >>> str(abjad.Fermata())
            '\\fermata'

        ..  container:: example

            Long fermata:

            >>> str(abjad.Fermata('longfermata'))
            '\\longfermata'

        """
        return rf"\{self.command}"

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

    @staticmethod
    def list_allowable_commands() -> typing.Tuple[str, ...]:
        """
        Lists allowable commands:

        ..  container:: example

            All allowable commands:

            >>> commands = abjad.Fermata.list_allowable_commands()
            >>> for command in commands:
            ...     command
            'fermata'
            'longfermata'
            'shortfermata'
            'verylongfermata'

        """
        return Fermata._allowable_commands


@dataclasses.dataclass(slots=True)
class Glissando:
    r"""
    LilyPond ``\glissando`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> glissando = abjad.Glissando()
        >>> abjad.tweak(glissando).color = "#blue"
        >>> abjad.attach(glissando, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \glissando
                d'4
                e'4
                f'4
            }

    ..  container:: example

        >>> abjad.Glissando()
        Glissando(allow_repeats=False, allow_ties=False, parenthesize_repeats=False, stems=False, style=None, tweaks=None, zero_padding=False)

    ..  container:: example

        Tweaks;

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> glissando = abjad.Glissando()
        >>> abjad.tweak(glissando).color = "#blue"
        >>> abjad.attach(glissando, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \glissando
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Set ``zero_padding=True`` when glissando formats with zero padding and no extra
        space for dots:

        >>> staff = abjad.Staff("d'8 d'4. d'4. d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     allow_repeats=True,
        ...     zero_padding=True,
        ... )
        >>> for note in staff[1:]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'8
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'8
            }

        >>> staff = abjad.Staff("c'8. d'8. e'8. f'8.")
        >>> abjad.glissando(
        ...     staff[:],
        ...     zero_padding=True,
        ... )
        >>> for note in staff[1:-1]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'8.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                e'8.
                - \abjad-zero-padding-glissando
                \glissando
                f'8.
            }

    """

    allow_repeats: bool = False
    allow_ties: bool = False
    parenthesize_repeats: bool = False
    stems: bool = False
    style: typing.Optional[str] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None
    zero_padding: bool = False

    _is_dataclass = True

    context = "Voice"
    persistent = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        strings = []
        if self.zero_padding:
            strings.append(r"- \abjad-zero-padding-glissando")
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            strings.extend(tweaks)
        strings.append(r"\glissando")
        bundle.after.spanner_starts.extend(strings)
        return bundle


@dataclasses.dataclass(slots=True)
class KeyCluster:
    r"""
    Key cluster.

    ..  container:: example

        Default values:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster()
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

    ..  container:: example

        Includes flat markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_flat_markup=True)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

        Default behavior.

    ..  container:: example

        Does not include flat markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_flat_markup=False)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \natural
            }

    ..  container:: example

        Includes natural markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_natural_markup=True)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

        Does not include natural markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_natural_markup=False)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \flat
            }

    ..  container:: example

        Key cluster formats LilyPond overrides instead of tweaks:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster()
        >>> abjad.attach(key_cluster, chord)
        >>> string = abjad.lilypond(chord)
        >>> print(string)
        \once \override Accidental.stencil = ##f
        \once \override AccidentalCautionary.stencil = ##f
        \once \override Arpeggio.X-offset = #-2
        \once \override NoteHead.stencil = #ly:text-interface::print
        \once \override NoteHead.text =
        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
        <c' e' g' b' d'' f''>8
        ^ \markup \center-align \concat { \natural \flat }

        The reason for this is that chords contain multiple note-heads: if key cluster
        formatted tweaks instead of overrides, the five format commands shown above would
        need to be duplicated immediately before each note-head.

    ..  container:: example

        Positions markup up:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(markup_direction=abjad.Up)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

        Positions markup down:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(markup_direction=abjad.Down)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                _ \markup \center-align \concat { \natural \flat }
            }

    """

    include_flat_markup: bool = True
    include_natural_markup: bool = True
    markup_direction: typing.Union[int, _enums.VerticalAlignment] = _enums.Up

    _is_dataclass = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        bundle.grob_overrides.append(
            "\\once \\override Accidental.stencil = ##f\n"
            "\\once \\override AccidentalCautionary.stencil = ##f\n"
            "\\once \\override Arpeggio.X-offset = #-2\n"
            "\\once \\override NoteHead.stencil = #ly:text-interface::print\n"
            "\\once \\override NoteHead.text =\n"
            "\\markup \\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25"
        )
        if self.include_flat_markup and self.include_natural_markup:
            string = r"\center-align \concat { \natural \flat }"
        elif self.include_flat_markup:
            string = r"\center-align \flat"
        else:
            string = r"\center-align \natural"
        markup = _markups.Markup(rf"\markup {string}", direction=self.markup_direction)
        markup_format_pieces = markup._get_format_pieces()
        bundle.after.markup.extend(markup_format_pieces)
        return bundle


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Mode:
    """
    Mode.

    ..  container:: example

        >>> abjad.Mode("major")
        Mode(mode_name='major')

    """

    mode_name: str = "major"

    _is_dataclass = True

    def named_interval_segment(self):
        mdi_segment = []
        m2 = _pitch.NamedInterval("m2")
        M2 = _pitch.NamedInterval("M2")
        A2 = _pitch.NamedInterval("aug2")
        dorian = [M2, m2, M2, M2, M2, m2, M2]
        if self.mode_name == "dorian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=0))
        elif self.mode_name == "phrygian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-1))
        elif self.mode_name == "lydian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-2))
        elif self.mode_name == "mixolydian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-3))
        elif self.mode_name in ("aeolian", "minor", "natural minor"):
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-4))
        elif self.mode_name == "locrian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-5))
        elif self.mode_name in ("ionian", "major"):
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-6))
        elif self.mode_name == "melodic minor":
            mdi_segment.extend([M2, m2, M2, M2, M2, M2, m2])
        elif self.mode_name == "harmonic minor":
            mdi_segment.extend([M2, m2, M2, M2, m2, A2, m2])
        else:
            raise ValueError(f"unknown mode name: {self.mode_name!r}.")
        return _pcollections.IntervalSegment(
            items=mdi_segment, item_class=_pitch.NamedInterval
        )


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class KeySignature:
    r"""
    Key signature.

    ..  container:: example

        >>> staff = abjad.Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = abjad.KeySignature("e", "major")
        >>> abjad.attach(key_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \key e \major
                e'8
                fs'8
                gs'8
                a'8
            }

    ..  container:: example

        >>> staff = abjad.Staff("e'8 fs'8 g'8 a'8")
        >>> key_signature = abjad.KeySignature("e", "minor")
        >>> abjad.attach(key_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \key e \minor
                e'8
                fs'8
                g'8
                a'8
            }

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> key = abjad.KeySignature("e", "minor")
        >>> abjad.tweak(key).color = "#blue"
        >>> abjad.attach(key, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak color #blue
                \key e \minor
                c'4
                d'4
                e'4
                f'4
            }

    """

    tonic: _pitch.NamedPitchClass = _pitch.NamedPitchClass("c")
    mode: Mode = Mode("major")
    tweaks: typing.Union[_overrides.TweakInterface, None] = None

    _is_dataclass = True

    context = "Staff"
    persistent = True
    redraw = True

    def __post_init__(self):
        if not isinstance(self.tonic, _pitch.NamedPitchClass):
            self.tonic = _pitch.NamedPitchClass(self.tonic)
        if not isinstance(self.mode, Mode):
            self.mode = Mode(self.mode)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        assert isinstance(self.mode, Mode), repr(self.mode)
        return rf"\key {self.tonic!s} \{self.mode.mode_name}"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.before.commands.extend(tweaks)
        bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    @property
    def name(self) -> str:
        """
        Gets name of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature("e", "major")
            >>> key_signature.name
            'E major'

            e minor:

            >>> key_signature = abjad.KeySignature("e", "minor")
            >>> key_signature.name
            'e minor'

        """
        assert isinstance(self.mode, Mode)
        if self.mode.mode_name == "major":
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return f"{tonic!s} {self.mode.mode_name}"


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class LaissezVibrer:
    r"""
    Laissez vibrer.

    ..  container:: example

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> laissez_vibrer = abjad.LaissezVibrer()
        >>> abjad.attach(laissez_vibrer, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' e' g' c''>4
            \laissezVibrer

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> lv = abjad.LaissezVibrer()
        >>> abjad.tweak(lv).color = "#blue"
        >>> abjad.attach(lv, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \laissezVibrer

    """

    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    _format_slot = "after"

    _time_orientation = _enums.Right

    def __str__(self) -> str:
        r"""
        Gets string representation of laissez vibrer indicator.

        ..  container:: example

            Default:

            >>> str(abjad.LaissezVibrer())
            '\\laissezVibrer'

        """
        return r"\laissezVibrer"

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class MarginMarkup:
    r"""
    Margin markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = abjad.MarginMarkup(
        ...     markup=abjad.Markup(r"\markup Vc.")
        ... )
        >>> abjad.attach(margin_markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set Staff.shortInstrumentName =
                \markup Vc.
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Set markup to externally defined command string like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = abjad.MarginMarkup(
        ...     markup=r"\my_custom_instrument_name",
        ... )
        >>> abjad.attach(margin_markup, staff[0])

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set Staff.shortInstrumentName = \my_custom_instrument_name
                c'4
                d'4
                e'4
                f'4
            }

    """

    context: str = "Staff"
    format_slot: str = "before"
    markup: typing.Union[str, _markups.Markup, None] = None

    _is_dataclass = True

    latent = True
    persistent = True
    redraw = True

    @property
    def _lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__

    def _get_lilypond_format(self, context=None):
        result = []
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._lilypond_type
        if isinstance(self.markup, _markups.Markup):
            markup = self.markup
            if markup.direction is not None:
                markup = dataclasses.replace(markup, direction=None)
            pieces = markup._get_format_pieces()
            result.append(rf"\set {context!s}.shortInstrumentName =")
            result.extend(pieces)
        else:
            assert isinstance(self.markup, str)
            string = rf"\set {context!s}.shortInstrumentName = {self.markup}"
            result.append(string)
        return result

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.extend(self._get_lilypond_format())
        return bundle


@functools.total_ordering
@dataclasses.dataclass(slots=True, unsafe_hash=True)
class MetronomeMark:
    r"""
    MetronomeMark.

    ..  container:: example

        Initializes integer-valued metronome mark:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo 4=90
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Initializes rational-valued metronome mark:

        >>> import quicktions
        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), quicktions.Fraction(272, 3))
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-mixed-number-markup #2 #0 #1 #"90" #"2" #"3"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

        Overrides rational-valued metronome mark with decimal string:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(272, 3),
        ...     decimal="90.66",
        ... )
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-markup #2 #0 #1 #"90.66"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

        Overrides rational-valued metronome mark with exact decimal:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(901, 10),
        ...     decimal=True,
        ... )
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-markup #2 #0 #1 #"90.1"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Initializes from text, duration and range:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), (120, 133), 'Quick')
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo Quick 4=120-133
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Custom markup:

        >>> import quicktions
        >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
        ...     abjad.Duration(1, 4),
        ...     67.5,
        ...  )
        >>> mark = abjad.MetronomeMark(
        ...     reference_duration=(1, 4),
        ...     units_per_minute=quicktions.Fraction(135, 2),
        ...     custom_markup=markup,
        ...  )
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-markup #2 #0 #1 #"67.5"
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        Decimal overrides:

        >>> import quicktions
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(272, 3),
        ... )
        >>> mark.decimal
        False

        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(272, 3),
        ...     decimal="90.66",
        ... )
        >>> mark.decimal
        '90.66'

        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(901, 10),
        ...     decimal=True,
        ... )
        >>> mark.decimal
        True

    ..  container:: example

        Set ``hide=True`` when metronome mark should not appear in output (but
        should still determine effective metronome mark):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> metronome_mark_1 = abjad.MetronomeMark((1, 4), 72)
        >>> abjad.attach(metronome_mark_1, staff[0])
        >>> metronome_mark_2 = abjad.MetronomeMark(
        ...     textual_indication='Allegro',
        ...     hide=True,
        ... )
        >>> abjad.attach(metronome_mark_2, staff[2])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new Staff
            {
                \tempo 4=72
                c'4
                d'4
                e'4
                f'4
            }
        >>

        >>> for leaf in abjad.iterate.leaves(staff):
        ...     prototype = abjad.MetronomeMark
        ...     leaf, abjad.get.effective(leaf, prototype)
        ...
        (Note("c'4"), MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=72, textual_indication=None, custom_markup=None, decimal=False, hide=False))
        (Note("d'4"), MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=72, textual_indication=None, custom_markup=None, decimal=False, hide=False))
        (Note("e'4"), MetronomeMark(reference_duration=None, units_per_minute=None, textual_indication='Allegro', custom_markup=None, decimal=False, hide=True))
        (Note("f'4"), MetronomeMark(reference_duration=None, units_per_minute=None, textual_indication='Allegro', custom_markup=None, decimal=False, hide=True))

    """

    reference_duration: typing.Optional[_typings.DurationTyping] = None
    units_per_minute: typing.Union[int, quicktions.Fraction] = None
    textual_indication: typing.Optional[str] = None
    custom_markup: typing.Optional[_markups.Markup] = None
    decimal: bool | str = False
    hide: bool = False

    _is_dataclass = True

    context = "Score"
    parameter = "METRONOME_MARK"
    persistent = True

    _format_slot = "opening"

    _mutates_offsets_in_seconds = True

    def __post_init__(self):
        assert isinstance(self.textual_indication, (str, type(None)))
        if self.reference_duration:
            self.reference_duration = _duration.Duration(self.reference_duration)
        if isinstance(self.units_per_minute, float):
            raise Exception(
                f"do not set units-per-minute to float ({self.units_per_minute});"
                " use fraction with decimal override instead."
            )
        prototype = (int, quicktions.Fraction, collections.abc.Sequence, type(None))
        assert isinstance(self.units_per_minute, prototype)
        if isinstance(self.units_per_minute, collections.abc.Sequence):
            assert len(self.units_per_minute) == 2
            item_prototype = (int, _duration.Duration)
            assert all(isinstance(_, item_prototype) for _ in self.units_per_minute)
            self.units_per_minute = tuple(sorted(self.units_per_minute))
        if self.custom_markup is not None:
            assert isinstance(self.custom_markup, _markups.Markup)
        if self.decimal is not None:
            assert isinstance(self.decimal, (bool, str)), repr(self.decimal)
        assert isinstance(self.hide, bool), repr(self.hide)

    def __eq__(self, argument) -> bool:
        """
        Is true when metronome mark equals ``argument``.

        ..  container:: example

            >>> mark_1 = abjad.MetronomeMark((3, 32), 52)
            >>> mark_2 = abjad.MetronomeMark((3, 32), 52)

            >>> mark_1 == mark_2
            True

            >>> mark_2 == mark_1
            True

        ..  container:: example

            >>> mark_1 = abjad.MetronomeMark((3, 32), 52)
            >>> mark_2 = abjad.MetronomeMark((6, 32), 104)

            >>> mark_1 == mark_2
            False

            >>> mark_2 == mark_1
            False

        ..  container:: example

            >>> mark_1 = abjad.MetronomeMark((3, 32), 52, 'Langsam')
            >>> mark_2 = abjad.MetronomeMark((3, 32), 52, 'Langsam')
            >>> mark_3 = abjad.MetronomeMark((3, 32), 52, 'Slow')

            >>> mark_1 == mark_2
            True

            >>> mark_1 == mark_3
            False

        """
        if not isinstance(argument, type(self)):
            return False
        # 'hide' is excluded from equality testing:
        if (
            self.reference_duration == argument.reference_duration
            and self.units_per_minute == argument.units_per_minute
            and self.textual_indication == argument.textual_indication
            and self.custom_markup == argument.custom_markup
        ):
            return True
        return False

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a metronome mark with quarters per minute greater
        than that of this metronome mark.
        """
        assert isinstance(argument, type(self)), repr(argument)
        self_quarters_per_minute = self.quarters_per_minute or 0
        argument_quarters_per_minute = argument.quarters_per_minute or 0
        assert isinstance(self_quarters_per_minute, (int, float, quicktions.Fraction))
        assert isinstance(
            argument_quarters_per_minute, (int, float, quicktions.Fraction)
        )
        return self_quarters_per_minute < argument_quarters_per_minute

    def __str__(self) -> str:
        """
        Gets string representation of metronome mark.

        ..  container:: example

            Integer-valued metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> str(mark)
            '4=90'

        ..  container:: example

            Rational-valued metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), (272, 3))
            >>> str(mark)
            '4=3-272'

        """
        if self.textual_indication is not None:
            string = self.textual_indication
        elif isinstance(self.units_per_minute, (int, float)):
            string = f"{self._dotted}={self.units_per_minute}"
        elif isinstance(
            self.units_per_minute, quicktions.Fraction
        ) and not _math.is_integer_equivalent_number(self.units_per_minute):
            integer_part = int(float(self.units_per_minute))
            remainder = self.units_per_minute - integer_part
            remainder = quicktions.Fraction(remainder)
            string = f"{self._dotted}={integer_part}+{remainder}"
        elif isinstance(
            self.units_per_minute, quicktions.Fraction
        ) and _math.is_integer_equivalent_number(self.units_per_minute):
            integer = int(float(self.units_per_minute))
            string = f"{self._dotted}={integer}"
        elif isinstance(self.units_per_minute, tuple):
            first = self.units_per_minute[0]
            second = self.units_per_minute[1]
            string = f"{self._dotted}={first}-{second}"
        else:
            raise TypeError(f"unknown: {self.units_per_minute!r}.")
        return string

    @property
    def _dotted(self):
        return self.reference_duration.lilypond_duration_string

    @property
    def _equation(self):
        if self.reference_duration is None:
            return
        if isinstance(self.units_per_minute, tuple):
            first, second = self.units_per_minute
            string = f"{self._dotted}={first}-{second}"
            return string
        elif isinstance(self.units_per_minute, quicktions.Fraction):
            markup = MetronomeMark.make_tempo_equation_markup(
                self.reference_duration,
                self.units_per_minute,
                decimal=self.decimal,
            )
            string = str(markup)
            return string
        string = f"{self._dotted}={self.units_per_minute}"
        return string

    def _get_lilypond_format(self):
        text, equation = None, None
        if self.textual_indication is not None:
            text = self.textual_indication
            assert isinstance(text, str)
            if " " in text:
                text = f'"{text}"'
        if self.reference_duration is not None and self.units_per_minute is not None:
            equation = self._equation
        if self.custom_markup is not None:
            return rf"\tempo {self.custom_markup}"
        elif text and equation:
            return rf"\tempo {text} {equation}"
        elif equation:
            return rf"\tempo {equation}"
        elif text:
            return rf"\tempo {text}"
        else:
            return r"\tempo \default"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if not self.hide:
            bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    def _get_markup(self):
        if self.custom_markup is not None:
            return self.custom_markup
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        stem_height = 1
        string = "abjad-metronome-mark-markup"
        string += f" #{duration_log}"
        string += f" #{self.reference_duration.dot_count}"
        string += f" #{stem_height}"
        string += f' #"{self.units_per_minute}"'
        markup = _markups.Markup(rf"\markup {string}")
        return markup

    # TODO: refactor to return dict
    def _get_markup_arguments(self):
        assert self.custom_markup is None
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        dot_count = self.reference_duration.dot_count
        stem_height = 1
        if not self.decimal:
            return (
                duration_log,
                dot_count,
                stem_height,
                self.units_per_minute,
            )
        if isinstance(self.decimal, str):
            return (duration_log, dot_count, stem_height, self.decimal)
        assert self.decimal is True, repr(self.decimal)
        # TODO: add abjad.NonreducedFraction.mixed_number property
        fraction = _duration.NonreducedFraction(self.units_per_minute)
        n, d = fraction.pair
        base = n // d
        n = n % d
        return (duration_log, dot_count, stem_height, base, n, d)

    @property
    def is_imprecise(self) -> bool:
        """
        Is true if metronome mark is entirely textual or if metronome mark's
        units_per_minute is a range.

        ..  container:: example

            Imprecise metronome marks:

            >>> abjad.MetronomeMark((1, 4), 60).is_imprecise
            False
            >>> abjad.MetronomeMark(4, 60, 'Langsam').is_imprecise
            False
            >>> abjad.MetronomeMark(textual_indication='Langsam').is_imprecise
            True
            >>> abjad.MetronomeMark(4, (35, 50), 'Langsam').is_imprecise
            True
            >>> abjad.MetronomeMark((1, 4), (35, 50)).is_imprecise
            True

            Precise metronome marks:

            >>> abjad.MetronomeMark((1, 4), 60).is_imprecise
            False

        """
        if self.reference_duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def quarters_per_minute(self) -> typing.Union[tuple, None, quicktions.Fraction]:
        """
        Gets metronome mark quarters per minute.

        ..  container:: example

            >>> mark = abjad.MetronomeMark((1, 8), 52)
            >>> mark.quarters_per_minute
            Fraction(104, 1)

        Gives tuple when metronome mark ``units_per_minute`` is a range.

        Gives none when metronome mark is imprecise.

        Gives fraction otherwise.
        """
        if self.is_imprecise:
            return None
        if isinstance(self.units_per_minute, tuple):
            low = (
                _duration.Duration(1, 4)
                / self.reference_duration
                * self.units_per_minute[0]
            )
            high = (
                _duration.Duration(1, 4)
                / self.reference_duration
                * self.units_per_minute[1]
            )
            return (low, high)
        result = (
            _duration.Duration(1, 4) / self.reference_duration * self.units_per_minute
        )
        return quicktions.Fraction(result)

    def duration_to_milliseconds(self, duration) -> _duration.Duration:
        """
        Gets millisecond value of ``duration`` under a given metronome mark.

        ..  container:: example

            Dotted sixteenth lasts 1500 msec at quarter equals 60:

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> mark.duration_to_milliseconds((3, 8))
            Duration(1500, 1)

        """
        assert isinstance(self.reference_duration, _duration.Duration)
        denominator = self.reference_duration.denominator
        numerator = self.reference_duration.numerator
        whole_note_duration = 1000
        whole_note_duration *= _duration.Multiplier(denominator, numerator)
        whole_note_duration *= _duration.Multiplier(60, self.units_per_minute)
        duration = _duration.Duration(duration)
        return _duration.Duration(duration * whole_note_duration)

    def list_related_tempos(
        self,
        maximum_numerator=None,
        maximum_denominator=None,
        integer_tempos_only=False,
    ) -> typing.List[typing.Tuple["MetronomeMark", "_ratio.Ratio"]]:
        r"""
        Lists related tempos.

        ..  container:: example

            Rewrites tempo ``4=58`` by ratios ``n:d`` such that ``1 <= n <= 8`` and ``1
            <= d <= 8``.

            >>> mark = abjad.MetronomeMark((1, 4), 58)
            >>> pairs = mark.list_related_tempos(
            ...     maximum_numerator=8,
            ...     maximum_denominator=8,
            ...  )

            >>> for tempo, ratio in pairs:
            ...     string = f'{tempo!s}    {ratio!s}'
            ...     print(string)
            4=29    1:2
            4=33+1/7    4:7
            4=34+4/5    3:5
            4=36+1/4    5:8
            4=38+2/3    2:3
            4=41+3/7    5:7
            4=43+1/2    3:4
            4=46+2/5    4:5
            4=48+1/3    5:6
            4=49+5/7    6:7
            4=50+3/4    7:8
            4=58    1:1
            4=66+2/7    8:7
            4=67+2/3    7:6
            4=69+3/5    6:5
            4=72+1/2    5:4
            4=77+1/3    4:3
            4=81+1/5    7:5
            4=87    3:2
            4=92+4/5    8:5
            4=96+2/3    5:3
            4=101+1/2    7:4
            4=116    2:1

        ..  container:: example

            Integer-valued tempos only:

            >>> mark = abjad.MetronomeMark((1, 4), 58)
            >>> pairs = mark.list_related_tempos(
            ...     maximum_numerator=16,
            ...     maximum_denominator=16,
            ...     integer_tempos_only=True,
            ...  )

            >>> for tempo, ratio in pairs:
            ...     string = f'{tempo!s}    {ratio!s}'
            ...     print(string)
            4=29    1:2
            4=58    1:1
            4=87    3:2
            4=116    2:1

        Constrains ratios such that ``1:2 <= n:d <= 2:1``.
        """
        allowable_numerators = range(1, maximum_numerator + 1)
        allowable_denominators = range(1, maximum_denominator + 1)
        numbers = [allowable_numerators, allowable_denominators]
        pairs = _enumerate.outer_product(numbers)
        multipliers = [_duration.Multiplier(_) for _ in pairs]
        multipliers = [
            _
            for _ in multipliers
            if quicktions.Fraction(1, 2) <= _ <= quicktions.Fraction(2)
        ]
        multipliers.sort()
        multipliers_ = _sequence.remove_repeats(multipliers)
        pairs = []
        for multiplier in multipliers_:
            new_units_per_minute = multiplier * self.units_per_minute
            if integer_tempos_only and not _math.is_integer_equivalent_number(
                new_units_per_minute
            ):
                continue
            metronome_mark = type(self)(
                reference_duration=self.reference_duration,
                units_per_minute=new_units_per_minute,
            )
            ratio = _ratio.Ratio(multiplier.pair)
            pair = (metronome_mark, ratio)
            pairs.append(pair)
        return pairs

    @staticmethod
    def make_tempo_equation_markup(
        reference_duration, units_per_minute, *, decimal=False
    ) -> _markups.Markup:
        r"""
        Makes tempo equation markup.

        ..  container:: example

            Integer-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup((1, 4),  90)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', markup])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \abjad-metronome-mark-markup #2 #0 #1 #"90"

        ..  container:: example

            Float-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup((1, 4), 90.1)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', markup])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \abjad-metronome-mark-markup #2 #0 #1 #"90.1"

        ..  container:: example

            Rational-valued metronome mark:

            >>> import quicktions
            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     abjad.Duration(1, 4),
            ...     quicktions.Fraction(272, 3),
            ... )
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', markup])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \abjad-metronome-mark-mixed-number-markup #2 #0 #1 #"90" #"2" #"3"

        """
        reference_duration_ = _duration.Duration(reference_duration)
        log = reference_duration_.exponent
        dots = reference_duration_.dot_count
        stem = 1
        if isinstance(
            units_per_minute, quicktions.Fraction
        ) and not _math.is_integer_equivalent_number(units_per_minute):
            if decimal:
                decimal_: typing.Union[float, str]
                if decimal is True:
                    decimal_ = float(units_per_minute)
                else:
                    assert isinstance(decimal, str), repr(decimal)
                    decimal_ = decimal
                markup = _markups.Markup(
                    r"\markup \abjad-metronome-mark-markup"
                    f' #{log} #{dots} #{stem} #"{decimal_}"'
                )
            else:
                nonreduced = _duration.NonreducedFraction(units_per_minute)
                base = int(nonreduced)
                remainder = nonreduced - base
                n, d = remainder.pair
                markup = _markups.Markup(
                    r"\markup \abjad-metronome-mark-mixed-number-markup"
                    f" #{log} #{dots} #{stem}"
                    f' #"{base}" #"{n}" #"{d}"'
                )
        else:
            markup = _markups.Markup(
                r"\markup \abjad-metronome-mark-markup"
                f' #{log} #{dots} #{stem} #"{units_per_minute}"'
            )
        return markup


@dataclasses.dataclass(slots=True)
class Ottava:
    r"""
    LilyPond ``\ottava`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> ottava = abjad.Ottava(n=1)
        >>> abjad.attach(ottava, staff[0])
        >>> ottava = abjad.Ottava(n=0, format_slot='after')
        >>> abjad.attach(ottava, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \ottava 1
                c'4
                d'4
                e'4
                f'4
                \ottava 0
            }

    """

    n: typing.Optional[int] = None
    format_slot: str = "before"

    _is_dataclass = True

    persistent = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        n = self.n or 0
        string = rf"\ottava {n}"
        if self.format_slot in ("before", None):
            bundle.before.commands.append(string)
        else:
            assert self.format_slot == "after"
            bundle.after.commands.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class RehearsalMark:
    r"""
    Rehearsal mark.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.RehearsalMark(number=1)
        >>> abjad.attach(mark, staff[0])
        >>> scheme = "#format-mark-box-alphabet"
        >>> abjad.setting(score).markFormatter = scheme
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                markFormatter = #format-mark-box-alphabet
            }
            <<
                \new Staff
                {
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>


    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> mark = abjad.RehearsalMark(markup='A')
        >>> abjad.tweak(mark).color = "#blue"
        >>> abjad.attach(mark, note)
        >>> staff = abjad.Staff([note])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak color #blue
                \mark A
                c'4
            }

    ..  container:: example

        Copy:

        >>> note = abjad.Note("c'4")
        >>> mark = abjad.RehearsalMark(markup='A')
        >>> abjad.tweak(mark).color = "#blue"
        >>> abjad.attach(mark, note)
        >>> staff = abjad.Staff([note])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak color #blue
                \mark A
                c'4
            }

    ..  container:: example

        Copy preserves tweaks:

        >>> import copy
        >>> mark = abjad.RehearsalMark(number=1)
        >>> abjad.tweak(mark).color = "#red"
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak color #red
                \mark #1
                c'4
                d'4
                e'4
                f'4
            }

        >>> mark = copy.copy(mark)
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak color #red
                \mark #1
                c'4
                d'4
                e'4
                f'4
            }

    """

    markup: typing.Union[_markups.Markup, str, None] = None
    number: typing.Union[int, None] = None
    tweaks: typing.Union[_overrides.TweakInterface, None] = None

    _is_dataclass = True

    context = "Score"

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        if self.markup is not None:
            result = rf"\mark {self.markup}"
        elif self.number is not None:
            result = rf"\mark #{self.number}"
        else:
            result = r"\mark \default"
        return result

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.opening.commands.extend(tweaks)
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    @staticmethod
    def from_string(string) -> "RehearsalMark":
        """
        Makes rehearsal mark from ``string``.

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('A')
            RehearsalMark(markup=None, number=1, tweaks=None)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('AA')
            RehearsalMark(markup=None, number=27, tweaks=None)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('AB')
            RehearsalMark(markup=None, number=28, tweaks=None)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('BA')
            RehearsalMark(markup=None, number=53, tweaks=None)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('BB')
            RehearsalMark(markup=None, number=54, tweaks=None)

        """
        number = 0
        for place, letter in enumerate(reversed(string)):
            integer = ord(letter) - ord("A") + 1
            multiplier = 26**place
            integer *= multiplier
            number += integer
        return RehearsalMark(number=number)


@dataclasses.dataclass(slots=True)
class Repeat:
    r"""
    Repeat.

    ..  container:: example

        Volta repeat:

        >>> container = abjad.Container("c'4 d'4 e'4 f'4")
        >>> repeat = abjad.Repeat()
        >>> abjad.attach(repeat, container)
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score)  # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \repeat volta 2
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

    ..  container:: example

        Unfold repeat:

        >>> container = abjad.Container("c'4 d'4 e'4 f'4")
        >>> repeat = abjad.Repeat(repeat_type='unfold')
        >>> abjad.attach(repeat, container)
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score)  # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \repeat unfold 2
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

    """

    repeat_count: int = 2
    repeat_type: str = "volta"

    _is_dataclass = True

    _can_attach_to_containers = True

    _format_leaf_children = False

    _format_slot = "before"

    context = "Score"

    def _get_lilypond_format(self):
        return rf"\repeat {self.repeat_type} {self.repeat_count}"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        bundle.before.commands.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class RepeatTie:
    r"""
    LilyPond ``\repeatTie`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> repeat_tie = abjad.RepeatTie()
        >>> abjad.tweak(repeat_tie).color = "#blue"
        >>> abjad.attach(repeat_tie, staff[1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'4
                - \tweak color #blue
                \repeatTie
                d'4
                d'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.logical_tie(leaf)
        ...
        (Note("c'4"), LogicalTie(items=[Note("c'4"), Note("c'4")]))
        (Note("c'4"), LogicalTie(items=[Note("c'4"), Note("c'4")]))
        (Note("d'4"), LogicalTie(items=[Note("d'4")]))
        (Note("d'4"), LogicalTie(items=[Note("d'4")]))

    ..  container:: example

        With ``direction`` unset:

        >>> staff = abjad.Staff("c'4 c'4 c''4 c''4")
        >>> tie = abjad.RepeatTie()
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[1])
        >>> tie = abjad.RepeatTie()
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'4
                - \tweak color #blue
                \repeatTie
                c''4
                c''4
                - \tweak color #blue
                \repeatTie
            }

        With ``direction=abjad.Up``:

        >>> staff = abjad.Staff("c'4 c'4 c''4 c''4")
        >>> tie = abjad.RepeatTie(direction=abjad.Up)
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[1])
        >>> tie = abjad.RepeatTie(direction=abjad.Up)
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'4
                - \tweak color #blue
                ^
                \repeatTie
                c''4
                c''4
                - \tweak color #blue
                ^
                \repeatTie
            }

        With ``direction=abjad.Down``:

        >>> staff = abjad.Staff("c'4 c'4 c''4 c''4")
        >>> tie = abjad.RepeatTie(direction=abjad.Down)
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[1])
        >>> tie = abjad.RepeatTie(direction=abjad.Down)
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'4
                - \tweak color #blue
                _
                \repeatTie
                c''4
                c''4
                - \tweak color #blue
                _
                \repeatTie
            }

    ..  container:: example

        Tweaks;

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> repeat_tie = abjad.RepeatTie()
        >>> abjad.tweak(repeat_tie).color = "#blue"
        >>> abjad.attach(repeat_tie, staff[1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'4
                - \tweak color #blue
                \repeatTie
                d'4
                d'4
            }

    """

    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    context = "Voice"
    persistent = True

    def __post_init__(self):
        self.direction = _string.to_tridirectional_ordinal_constant(self.direction)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _attachment_test_all(self, argument):
        if not (
            hasattr(argument, "written_pitch") or hasattr(argument, "written_pitches")
        ):
            string = f"Must be note or chord (not {argument})."
            return [string]
        return True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            strings = self.tweaks._list_format_contributions()
            bundle.after.spanners.extend(strings)
        strings = []
        if self.direction is not None:
            string = _string.to_tridirectional_lilypond_symbol(self.direction)
            strings.append(string)
        strings.append(r"\repeatTie")
        bundle.after.spanners.extend(strings)
        return bundle


@dataclasses.dataclass(slots=True)
class StaffChange:
    r"""
    Staff change.

    ..  container:: example

        Explicit staff change:

        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.lilypond_type = "PianoStaff"
        >>> rh_staff = abjad.Staff("c'8 d'8 e'8 f'8", name="RH_Staff")
        >>> lh_staff = abjad.Staff("s2", name="LH_Staff")
        >>> staff_group.extend([rh_staff, lh_staff])
        >>> staff_change = abjad.StaffChange("LH_Staff")
        >>> abjad.attach(staff_change, rh_staff[2])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \context Staff = "RH_Staff"
                {
                    c'8
                    d'8
                    \change Staff = LH_Staff
                    e'8
                    f'8
                }
                \context Staff = "LH_Staff"
                {
                    s2
                }
            >>

    ..  container:: example

        Default staff change:

        >>> staff_change = abjad.StaffChange()
        >>> staff_change.staff is None
        True

        Explicit staff change:

        >>> lh_staff = abjad.Staff("s2", name="LH_Staff")
        >>> staff_change = abjad.StaffChange("LH_Staff")
        >>> staff_change.staff
        'LH_Staff'

    """

    staff: typing.Union[str, None] = None

    _is_dataclass = True
    context = "Staff"
    _format_leaf_children = False
    _format_slot = "opening"
    _time_orientation = _enums.Right

    def _get_lilypond_format(self):
        if self.staff is None:
            return r"\change Staff = ##f"
        assert isinstance(self.staff, str), repr(self.staff)
        return rf"\change Staff = {self.staff}"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class StartBeam:
    r"""
    LilyPond ``[`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> start_beam = abjad.StartBeam()
        >>> abjad.tweak(start_beam).color = "#blue"
        >>> abjad.attach(start_beam, staff[0])
        >>> stop_beam = abjad.StopBeam()
        >>> abjad.attach(stop_beam, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                - \tweak color #blue
                [
                d'8
                e'8
                f'8
                ]
            }

    ..  container:: example

        >>> abjad.StartBeam()
        StartBeam(direction=None, tweaks=None)

    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_beam = abjad.StartBeam()
        >>> abjad.tweak(start_beam).color = "#blue"
        >>> start_beam
        StartBeam(direction=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> start_beam_2 = copy.copy(start_beam)
        >>> start_beam_2
        StartBeam(direction=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True
    context = "Voice"
    parameter = "BEAM"
    persistent = True
    spanner_start = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _add_direction(self, string):
        if getattr(self, "direction", None) is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(self.direction)
            string = f"{symbol} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction("[")
        bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StartGroup:
    r"""
    LilyPond ``\startGroup`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_group = abjad.StartGroup()
        >>> abjad.tweak(start_group).color = "#blue"
        >>> abjad.attach(start_group, staff[0])
        >>> stop_group = abjad.StopGroup()
        >>> abjad.attach(stop_group, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
            }

    ..  container:: example

        >>> abjad.StartGroup()
        StartGroup(tweaks=None)

    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_group = abjad.StartGroup()
        >>> abjad.tweak(start_group).color = "#blue"
        >>> start_group
        StartGroup(tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> start_group_2 = copy.copy(start_group)
        >>> start_group_2
        StartGroup(tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True
    persistent = True
    spanner_start = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = r"\startGroup"
        bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StartHairpin:
    r"""
    Hairpin indicator.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \p
                \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        Crescendo:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \p
                \<
                d'4
                e'4
                f'4
                \f
            }

        Crescendo dal niente:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
        >>> abjad.attach(abjad.StartHairpin('o<'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                - \tweak circled-tip ##t
                \<
                d'4
                e'4
                f'4
                \f
            }

        Subito crescendo:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('<|'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \p
                - \tweak stencil #abjad-flared-hairpin
                \<
                d'4
                e'4
                f'4
                \f
            }

        Subito crescendo dal niente:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
        >>> abjad.attach(abjad.StartHairpin('o<|'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                - \tweak circled-tip ##t
                - \tweak stencil #abjad-flared-hairpin
                \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        Decrescendo:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('f'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('>'), staff[0])
        >>> abjad.attach(abjad.Dynamic('p'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \f
                \>
                d'4
                e'4
                f'4
                \p
            }

        Decrescendo al niente:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('f'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('>o'), staff[0])
        >>> abjad.attach(abjad.Dynamic('niente', command=r'\!'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \f
                - \tweak circled-tip ##t
                \>
                d'4
                e'4
                f'4
                \!
            }

        Subito decrescendo:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('f'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('|>'), staff[0])
        >>> abjad.attach(abjad.Dynamic('p'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \f
                - \tweak stencil #abjad-flared-hairpin
                \>
                d'4
                e'4
                f'4
                \p
            }

        Subito decrescendo al niente:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('f'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('|>o'), staff[0])
        >>> abjad.attach(abjad.Dynamic('niente', command=r'\!'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \f
                - \tweak circled-tip ##t
                - \tweak stencil #abjad-flared-hairpin
                \>
                d'4
                e'4
                f'4
                \!
            }

    ..  container:: example

        Constante:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('--'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \p
                - \tweak stencil #constante-hairpin
                \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.tweak(start_hairpin).color = "#blue"
        >>> abjad.attach(start_hairpin, staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
            }
            {
                c'4
                \p
                - \tweak color #blue
                \<
                d'4
                e'4
                f'4
                \f
            }

    """

    shape: str = "<"
    direction: int | _enums.VerticalAlignment | None = None
    tweaks: _overrides.TweakInterface | None = None

    _is_dataclass = True
    context = "Voice"
    parameter = "DYNAMIC"
    persistent = True
    spanner_start = True
    trend = True

    _crescendo_start = r"\<"

    _decrescendo_start = r"\>"

    _format_slot = "after"

    _known_shapes = ("<", "o<", "<|", "o<|", ">", ">o", "|>", "|>o", "--")

    # TODO: remove?
    _time_orientation = _enums.Right

    def __post_init__(self):
        self.direction = _string.to_tridirectional_ordinal_constant(self.direction)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _add_direction(self, string):
        if getattr(self, "direction", False):
            symbol = _string.to_tridirectional_lilypond_symbol(self.direction)
            string = f"{symbol} {string}"
        return string

    @staticmethod
    def _circled_tip():
        return _overrides.LilyPondOverride(
            grob_name="Hairpin",
            once=True,
            property_path="circled-tip",
            value=True,
        )

    @staticmethod
    def _constante_hairpin():
        return _overrides.LilyPondOverride(
            grob_name="Hairpin",
            once=True,
            property_path="stencil",
            value="#constante-hairpin",
        )

    @staticmethod
    def _flared_hairpin():
        return _overrides.LilyPondOverride(
            grob_name="Hairpin",
            once=True,
            property_path="stencil",
            value="#abjad-flared-hairpin",
        )

    def _get_lilypond_format(self):
        strings = []
        if "--" in self.shape:
            override = self._constante_hairpin()
            string = override.tweak_string()
            strings.append(string)
        if "o" in self.shape:
            override = self._circled_tip()
            string = override.tweak_string()
            strings.append(string)
        if "|" in self.shape:
            override = self._flared_hairpin()
            string = override.tweak_string()
            strings.append(string)
        if "<" in self.shape or "--" in self.shape:
            string = self._crescendo_start
            string = self._add_direction(string)
            strings.append(string)
        elif ">" in self.shape:
            string = self._decrescendo_start
            string = self._add_direction(string)
            strings.append(string)
        else:
            raise ValueError(self.shape)
        return strings

    def _get_lilypond_format_bundle(self, component=None):
        r"""
        hairpin contributes formatting to the 'spanners' slot
        (rather than the 'commands' slot). The reason for this is that
        the LilyPond \startTrillSpan [pitch] command must appear after
        \< and \> but before \set and other commmands.
        """
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanners.extend(tweaks)
        strings = self._get_lilypond_format()
        bundle.after.spanners.extend(strings)
        return bundle

    @property
    def known_shapes(self) -> typing.Tuple[str, ...]:
        r"""

        Gets known shapes.

        ..  container:: example

            >>> for shape in abjad.StartHairpin().known_shapes:
            ...     shape
            '<'
            'o<'
            '<|'
            'o<|'
            '>'
            '>o'
            '|>'
            '|>o'
            '--'

        """
        return self._known_shapes


@dataclasses.dataclass(unsafe_hash=True, slots=True)
class StartMarkup:
    r"""
    Start markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> markup = abjad.Markup(r"\markup Cellos")
        >>> start_markup = abjad.StartMarkup(markup=markup)
        >>> abjad.attach(start_markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set Staff.instrumentName =
                \markup Cellos
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Set instrument name to custom-defined LilyPond function like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> start_markup = abjad.StartMarkup(markup=r'\my_instrument_name')
        >>> abjad.attach(start_markup, staff[0])

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            \set Staff.instrumentName = \my_instrument_name
            c'4
            d'4
            e'4
            f'4
        }

    ..  container:: example

        Equality testing:

        >>> start_markup_1 = abjad.StartMarkup(
        ...     context='PianoStaff',
        ...     markup=abjad.Markup(r"\markup Harp"),
        ...     )
        >>> start_markup_2 = abjad.StartMarkup(
        ...     context="PianoStaff",
        ...     markup=abjad.Markup(r"\markup Harp"),
        ...     )
        >>> start_markup_3 = abjad.StartMarkup(
        ...     context="Staff",
        ...     markup=abjad.Markup(r"\markup Harp"),
        ...     )

        >>> start_markup_1 == start_markup_1
        True
        >>> start_markup_1 == start_markup_2
        True
        >>> start_markup_1 == start_markup_3
        False

        >>> start_markup_2 == start_markup_1
        True
        >>> start_markup_2 == start_markup_2
        True
        >>> start_markup_2 == start_markup_3
        False

        >>> start_markup_3 == start_markup_1
        False
        >>> start_markup_3 == start_markup_2
        False
        >>> start_markup_3 == start_markup_3
        True

    """

    markup: typing.Union[str, _markups.Markup] = "instrument name"
    context: str = "Staff"
    format_slot: str = "before"

    _is_dataclass = True

    @property
    def _lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__

    def _get_lilypond_format(self, context=None):
        result = []
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._lilypond_type
        if isinstance(self.markup, _markups.Markup):
            markup = self.markup
            if markup.direction is not None:
                markup = dataclasses.replace(markup, direction=None)
            pieces = markup._get_format_pieces()
            result.append(rf"\set {context!s}.instrumentName =")
            result.extend(pieces)
        else:
            assert isinstance(self.markup, str)
            string = rf"\set {context!s}.instrumentName = {self.markup}"
            result.append(string)
        return result

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.extend(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class StartPhrasingSlur:
    r"""
    LilyPond ``(`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> abjad.tweak(start_phrasing_slur).color = "#blue"
        >>> abjad.attach(start_phrasing_slur, staff[0])
        >>> stop_phrasing_slur = abjad.StopPhrasingSlur()
        >>> abjad.attach(stop_phrasing_slur, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \(
                d'4
                e'4
                f'4
                \)
            }

    ..  container:: example

        >>> abjad.StartPhrasingSlur()
        StartPhrasingSlur(direction=None, tweaks=None)

    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> abjad.tweak(start_phrasing_slur).color = "#blue"
        >>> start_phrasing_slur
        StartPhrasingSlur(direction=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> start_phrasing_slur_2 = copy.copy(start_phrasing_slur)
        >>> start_phrasing_slur_2
        StartPhrasingSlur(direction=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    context = "Voice"
    parameter = "PHRASING_SLUR"
    persistent = True
    spanner_start = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _add_direction(self, string):
        if getattr(self, "direction", False):
            symbol = _string.to_tridirectional_lilypond_symbol(self.direction)
            string = f"{symbol} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction(r"\(")
        bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StartPianoPedal:
    r"""
    LilyPond ``\sustainOn``, ``\sostenutoOn``, ``\unaCorda`` commands.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#blue"
        >>> abjad.tweak(start_piano_pedal).parent_alignment_X = abjad.Center
        >>> abjad.attach(start_piano_pedal, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[1])

        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#red"
        >>> abjad.attach(start_piano_pedal, staff[1])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[2])

        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#green"
        >>> abjad.attach(start_piano_pedal, staff[2])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[3])

        >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
        >>> abjad.setting(staff).pedalSustainStyle = "#'mixed"
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = 5
                pedalSustainStyle = #'mixed
            }
            {
                c'4
                - \tweak color #blue
                - \tweak parent-alignment-X #center
                \sustainOn
                d'4
                \sustainOff
                - \tweak color #red
                \sustainOn
                e'4
                \sustainOff
                - \tweak color #green
                \sustainOn
                r4
                \sustainOff
            }

    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#blue"
        >>> start_piano_pedal
        StartPianoPedal(kind=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> start_piano_pedal_2 = copy.copy(start_piano_pedal)
        >>> start_piano_pedal_2
        StartPianoPedal(kind=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    kind: str | None = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True
    context = "StaffGroup"
    parameter = "PEDAL"
    persistent = True
    spanner_start = True

    def __post_init__(self):
        if self.kind is not None:
            assert self.kind in ("sustain", "sostenuto", "corda"), repr(self.kind)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        if self.kind == "corda":
            string = r"\unaCorda"
        elif self.kind == "sostenuto":
            string = r"\sostenutoOn"
        else:
            assert self.kind in ("sustain", None)
            string = r"\sustainOn"
        bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StartSlur:
    r"""
    LilyPond ``(`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_slur = abjad.StartSlur()
        >>> abjad.tweak(start_slur).color = "#blue"
        >>> abjad.attach(start_slur, staff[0])
        >>> stop_slur = abjad.StopSlur()
        >>> abjad.attach(stop_slur, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                (
                d'4
                e'4
                f'4
                )
            }

    ..  container:: example

        >>> abjad.StartSlur()
        StartSlur(direction=None, tweaks=None)

    ..  container:: example

        With ``direction`` unset:

        >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
        >>> abjad.attach(abjad.StartSlur(), staff[0])
        >>> abjad.attach(abjad.StopSlur(), staff[3])
        >>> abjad.attach(abjad.StartSlur(), staff[4])
        >>> abjad.attach(abjad.StopSlur(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                (
                d'8
                e'8
                f'8
                )
                c''8
                (
                d''8
                e''8
                f''8
                )
            }

        With ``direction=abjad.Up``:

        >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
        >>> abjad.attach(abjad.StartSlur(direction=abjad.Up), staff[0])
        >>> abjad.attach(abjad.StopSlur(), staff[3])
        >>> abjad.attach(abjad.StartSlur(direction=abjad.Up), staff[4])
        >>> abjad.attach(abjad.StopSlur(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                ^ (
                d'8
                e'8
                f'8
                )
                c''8
                ^ (
                d''8
                e''8
                f''8
                )
            }

        With ``direction=abjad.Down``:

        >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
        >>> abjad.attach(abjad.StartSlur(direction=abjad.Down), staff[0])
        >>> abjad.attach(abjad.StopSlur(), staff[3])
        >>> abjad.attach(abjad.StartSlur(direction=abjad.Down), staff[4])
        >>> abjad.attach(abjad.StopSlur(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                _ (
                d'8
                e'8
                f'8
                )
                c''8
                _ (
                d''8
                e''8
                f''8
                )
            }

    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_slur = abjad.StartSlur()
        >>> abjad.tweak(start_slur).color = "#blue"
        >>> start_slur
        StartSlur(direction=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> start_slur_2 = copy.copy(start_slur)
        >>> start_slur_2
        StartSlur(direction=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True
    context = "Voice"
    parameter = "SLUR"
    persistent = True
    spanner_start = True

    def __post_init__(self):
        self.direction = _string.to_tridirectional_ordinal_constant(self.direction)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _add_direction(self, string):
        if getattr(self, "direction", None) is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(self.direction)
            string = f"{symbol} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction("(")
        bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StartTextSpan:
    r"""
    LilyPond ``\startTextSpan`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="solid-line-with-arrow",
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> abjad.StartTextSpan()
        StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, direction=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None, tweaks=None)

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")

        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> abjad.tweak(start_text_span).color = "#blue"
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])

        >>> start_text_span = abjad.StartTextSpan(
        ...     command=r"\startTextSpanOne",
        ...     left_text=abjad.Markup(r"\upright A"),
        ...     right_text=abjad.Markup(r"\markup \upright B"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> abjad.tweak(start_text_span).color = "#red"
        >>> abjad.tweak(start_text_span).staff_padding = 6
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan(command=r"\stopTextSpanOne")
        >>> abjad.attach(stop_text_span, staff[-1])

        >>> markup = abjad.Markup(r"\markup SPACER", direction=abjad.Up)
        >>> abjad.tweak(markup).transparent = True
        >>> abjad.attach(markup, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak transparent ##t
                ^ \markup SPACER
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak color #blue
                - \tweak staff-padding 2.5
                \startTextSpan
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright A \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright B
                - \tweak color #red
                - \tweak staff-padding 6
                \startTextSpanOne
                d'4
                e'4
                f'4
                \stopTextSpan
                \stopTextSpanOne
            }

        (Spacer text included to prevent docs from clipping output.)

    ..  container:: example

        String literals are allowed in place of markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> left_text = r'- \tweak bound-details.left.text \markup'
        >>> left_text += r' \concat { \upright pont. \hspace #0.5 }'
        >>> right_text = r'- \tweak bound-details.right.text \markup'
        >>> right_text += r' \upright tasto'
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=left_text,
        ...     right_text=right_text,
        ...     style='solid-line-with-arrow',
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Styles:

        >>> staff = abjad.Staff("c'4 d' e' fs'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                fs'4
                \stopTextSpan
            }

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     style="dashed-line-with-hook",
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-dashed-line-with-hook
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="invisible-line",
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-invisible-line
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="solid-line-with-arrow",
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     style="solid-line-with-hook",
        ... )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-solid-line-with-hook
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

        Styles constrained to ``'dashed-line-with-arrow'``, ``'dashed-line-with-hook'``,
        ``'invisible-line'``, ``'solid-line-with-arrow'``, ``'solid-line-with-hook'``,
        none.


    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_text_span = abjad.StartTextSpan(
        ...     style='dashed-line-with-arrow',
        ... )
        >>> abjad.tweak(start_text_span).color = "#blue"
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> start_text_span
        StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, direction=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style='dashed-line-with-arrow', tweaks=TweakInterface(('_literal', False), ('color', '#blue'), ('staff_padding', 2.5)))

        >>> start_text_span_2 = copy.copy(start_text_span)
        >>> start_text_span_2
        StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, direction=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style='dashed-line-with-arrow', tweaks=TweakInterface(('_literal', False), ('color', '#blue'), ('staff_padding', 2.5)))

    """

    command: str = r"\startTextSpan"
    concat_hspace_left: int | float = 0.5
    concat_hspace_right: int | float | None = None
    direction: int | _enums.VerticalAlignment | None = None
    left_broken_text: bool | str | _markups.Markup | None = None
    left_text: str | _markups.Markup | None = None
    right_padding: int | float | None = None
    right_text: str | _markups.Markup | None = None
    style: str | None = None
    tweaks: _overrides.TweakInterface | None = None

    _is_dataclass = True
    context = "Voice"
    parameter = "TEXT_SPANNER"
    persistent = True
    spanner_start = True

    _styles = (
        "dashed-line-with-arrow",
        "dashed-line-with-hook",
        "dashed-line-with-up-hook",
        "invisible-line",
        "solid-line-with-arrow",
        "solid-line-with-hook",
        "solid-line-with-up-hook",
    )

    def _add_direction(self, string):
        if getattr(self, "direction", False):
            symbol = _string.to_tridirectional_lilypond_symbol(self.direction)
            string = f"{symbol} {string}"
        return string

    def _get_left_broken_text_tweak(self):
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "left-broken", "text"),
            value=self.left_broken_text,
        )
        string = override.tweak_string(self)
        return string

    def _get_left_text_directive(self):
        if isinstance(self.left_text, str):
            return self.left_text
        left_text_string = self.left_text.string
        left_text_string = left_text_string.removeprefix(r"\markup").strip()
        hspace_string = rf"\hspace #{self.concat_hspace_left}"
        markup = _markups.Markup(
            rf"\markup \concat {{ {left_text_string} {hspace_string} }}"
        )
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "left", "text"),
            value=markup,
        )
        string = override.tweak_string()
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.style is not None:
            string = rf"- \abjad-{self.style}"
            bundle.after.spanner_starts.append(string)
        if self.left_text:
            string = self._get_left_text_directive()
            bundle.after.spanner_starts.append(string)
        if self.left_broken_text is not None:
            string = self._get_left_broken_text_tweak()
            bundle.after.spanner_starts.append(string)
        if self.right_text:
            string = self._get_right_text_tweak()
            bundle.after.spanner_starts.append(string)
        if self.right_padding:
            string = self._get_right_padding_tweak()
            bundle.after.spanner_starts.append(string)
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction(self.command)
        bundle.after.spanner_starts.append(string)
        return bundle

    def _get_right_padding_tweak(self):
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "right", "padding"),
            value=self.right_padding,
        )
        string = override.tweak_string()
        return string

    def _get_right_text_tweak(self):
        if isinstance(self.right_text, str):
            # TODO: is right_text ever set to string?
            #       should right_text be forced to always be a string? never markup?
            return self.right_text
        if self.concat_hspace_right is not None:
            number = self.concat_hspace_right
            right_text = self.right_text.string
            markup = _markups.Markup(
                rf"\markup \concat {{ {right_text} \hspace #{number} }}"
            )
        else:
            markup = self.right_text
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "right", "text"),
            value=markup,
        )
        string = override.tweak_string()
        return string

    def _get_start_command(self):
        string = self._get_parameter_name()
        return rf"\start{string}"


@dataclasses.dataclass(slots=True)
class StartTrillSpan:
    r"""
    LilyPond ``\startTrillSpan`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_trill_span = abjad.StartTrillSpan()
        >>> abjad.tweak(start_trill_span).color = "#blue"
        >>> abjad.attach(start_trill_span, staff[0])
        >>> stop_trill_span = abjad.StopTrillSpan()
        >>> abjad.attach(stop_trill_span, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startTrillSpan
                d'4
                e'4
                f'4
                \stopTrillSpan
            }

    ..  container:: example

        With interval:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_trill_span = abjad.StartTrillSpan(interval='M2')
        >>> abjad.tweak(start_trill_span).color = "#blue"
        >>> abjad.attach(start_trill_span, staff[0])
        >>> stop_trill_span = abjad.StopTrillSpan()
        >>> abjad.attach(stop_trill_span, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \pitchedTrill
                c'4
                - \tweak color #blue
                \startTrillSpan d'
                d'4
                e'4
                f'4
                \stopTrillSpan
            }

    ..  container:: example

        With pitch:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_trill_span = abjad.StartTrillSpan(pitch='C#4')
        >>> abjad.tweak(start_trill_span).color = "#blue"
        >>> abjad.attach(start_trill_span, staff[0])
        >>> stop_trill_span = abjad.StopTrillSpan()
        >>> abjad.attach(stop_trill_span, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \pitchedTrill
                c'4
                - \tweak color #blue
                \startTrillSpan cs'
                d'4
                e'4
                f'4
                \stopTrillSpan
            }

    ..  container:: example

        Tweaks survive copy:

        >>> import copy
        >>> start_trill_span = abjad.StartTrillSpan()
        >>> abjad.tweak(start_trill_span).color = "#blue"
        >>> start_trill_span
        StartTrillSpan(interval=None, pitch=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> start_trill_span_2 = copy.copy(start_trill_span)
        >>> start_trill_span_2
        StartTrillSpan(interval=None, pitch=None, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    interval: str | _pitch.NamedInterval | None = None
    pitch: str | _pitch.NamedPitch | None = None
    tweaks: _overrides.TweakInterface | None = None

    _is_dataclass = True
    context = "Voice"
    parameter = "TRILL"
    persistent = True
    spanner_start = True

    def __post_init__(self):
        if self.interval is not None:
            self.interval = _pitch.NamedInterval(self.interval)
        if self.pitch is not None:
            self.pitch = _pitch.NamedPitch(self.pitch)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = r"\startTrillSpan"
        if self.interval or self.pitch:
            bundle.opening.spanners.append(r"\pitchedTrill")
            if self.pitch:
                pitch = self.pitch
            else:
                pitch = component.written_pitch + self.interval
            string = string + f" {pitch!s}"
        bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StemTremolo:
    r"""
    Stem tremolo.

    ..  container:: example

        Sixteenth-note tremolo:

        >>> note = abjad.Note("c'4")
        >>> stem_tremolo = abjad.StemTremolo(16)
        >>> abjad.attach(stem_tremolo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            :16

    ..  container:: example

        Thirty-second-note tremolo:

        >>> note = abjad.Note("c'4")
        >>> stem_tremolo = abjad.StemTremolo(32)
        >>> abjad.attach(stem_tremolo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            :32

    ..  container:: example

        REGRESSION. Consider a note, rest, chord to which a stem tremolo is attached.
        When such a note, rest, chord splits into two notes, rests, chords then a stem
        tremolo attaches to each of the resultant notes, rests, chords:

        >>> staff = abjad.Staff("c'4 c'2.")
        >>> abjad.attach(abjad.StemTremolo(), staff[1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'2.
                :16
            }

        >>> abjad.Meter.rewrite_meter(staff[:], abjad.Meter((3, 4)))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                c'2
                :16
                ~
                c'4
                :16
            }

    """

    tremolo_flags: int = 16

    _is_dataclass = True

    _format_slot = "after"
    _time_orientation = _enums.Middle

    def __post_init__(self):
        if not _math.is_nonnegative_integer_power_of_two(self.tremolo_flags):
            raise ValueError(f"nonnegative integer power of 2: {self.tremolo_flags!r}.")

    def _get_lilypond_format(self):
        return f":{self.tremolo_flags!s}"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        bundle.after.stem_tremolos.append(self._get_lilypond_format())
        return bundle


@dataclasses.dataclass(slots=True)
class StopBeam:
    r"""
    LilyPond ``]`` command.

    ..  container:: example

        >>> abjad.StopBeam()
        StopBeam(leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'8 d' e' r")
        >>> start_beam = abjad.StartBeam()
        >>> abjad.tweak(start_beam).color = "#blue"
        >>> abjad.attach(start_beam, staff[0])
        >>> stop_beam = abjad.StopBeam()
        >>> abjad.attach(stop_beam, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                - \tweak color #blue
                [
                d'8
                e'8
                ]
                r8
            }

        With leak:

        >>> staff = abjad.Staff("c'8 d' e' r")
        >>> command = abjad.StartBeam()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopBeam(leak=True)
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                - \tweak color #blue
                [
                d'8
                e'8
                <> ]
                r8
            }

    """

    leak: bool = False

    _is_dataclass = True
    context = "Voice"
    parameter = "BEAM"
    persistent = True
    spanner_stop = True

    _time_orientation = _enums.Right

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = "]"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            # bundle.after.spanner_stops.append(string)
            # starts (instead of stops) so [ ] is possible on single leaf:
            bundle.after.spanner_starts.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StopGroup:
    r"""
    LilyPond ``\stopGroup`` command.

    ..  container:: example

        >>> abjad.StopGroup()
        StopGroup(leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartGroup()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopGroup()
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startGroup
                d'4
                e'4
                \stopGroup
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartGroup()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopGroup(leak=True)
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startGroup
                d'4
                e'4
                <> \stopGroup
                r4
            }

    ..  container:: example

        REGRESSION. Leaked contributions appear last in postevent format
        slot:

        >>> staff = abjad.Staff("c'8 d' e' f' r2")
        >>> abjad.beam(staff[:4])
        >>> command = abjad.StartGroup()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopGroup(leak=True)
        >>> abjad.attach(command, staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                - \tweak color #blue
                \startGroup
                d'8
                e'8
                f'8
                ]
                <> \stopGroup
                r2
            }

        The leaked text spanner above does not inadvertantly leak the beam.

    """

    leak: bool = False

    _is_dataclass = True
    persistent = True
    spanner_stop = True

    _time_orientation = _enums.Right

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = r"\stopGroup"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StopHairpin:
    r"""
    LilyPond ``\!`` command.

    ..  container:: example

        >>> abjad.StopHairpin()
        StopHairpin(leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.tweak(start_hairpin).color = "#blue"
        >>> abjad.attach(start_hairpin, staff[0])
        >>> stop_hairpin = abjad.StopHairpin()
        >>> abjad.attach(stop_hairpin, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \<
                d'4
                e'4
                \!
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> abjad.tweak(start_hairpin).color = "#blue"
        >>> abjad.attach(start_hairpin, staff[0])
        >>> stop_hairpin = abjad.StopHairpin(leak=True)
        >>> abjad.attach(stop_hairpin, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \<
                d'4
                e'4
                <> \!
                r4
            }

    """

    leak: bool = False

    _is_dataclass = True
    context = "Voice"
    # parameter = 'DYNAMIC'
    # persistent = True
    spanner_stop = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = r"\!"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            # bundle.after.spanner_stops.append(string)
            bundle.after.articulations.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StopPhrasingSlur:
    r"""
    LilyPond ``\)`` command.

    ..  container:: example

        >>> abjad.StopPhrasingSlur()
        StopPhrasingSlur(leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartPhrasingSlur()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopPhrasingSlur()
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \(
                d'4
                e'4
                \)
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartPhrasingSlur()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopPhrasingSlur(leak=True)
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \(
                d'4
                e'4
                <> \)
                r4
            }

    ..  container:: example

        REGRESSION. Leaked contributions appear last in postevent format
        slot:

        >>> staff = abjad.Staff("c'8 d' e' f' r2")
        >>> abjad.beam(staff[:4])
        >>> command = abjad.StartPhrasingSlur()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopPhrasingSlur(leak=True)
        >>> abjad.attach(command, staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                - \tweak color #blue
                \(
                d'8
                e'8
                f'8
                ]
                <> \)
                r2
            }

        The leaked text spanner above does not inadvertantly leak the beam.

    """

    leak: bool = False

    _is_dataclass = True
    context = "Voice"
    parameter = "PHRASING_SLUR"
    persistent = True
    spanner_stop = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = r"\)"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StopPianoPedal:
    r"""
    LilyPond ``\sostenutoOff``, ``\sustainOff``, ``\treCorde`` commands.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#blue"
        >>> abjad.tweak(start_piano_pedal).parent_alignment_X = abjad.Center
        >>> abjad.attach(start_piano_pedal, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.tweak(stop_piano_pedal).color = "#red"
        >>> abjad.tweak(stop_piano_pedal).parent_alignment_X = abjad.Center
        >>> abjad.attach(stop_piano_pedal, staff[-2])
        >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = 5
            }
            {
                c'4
                - \tweak color #blue
                - \tweak parent-alignment-X #center
                \sustainOn
                d'4
                e'4
                - \tweak color #red
                - \tweak parent-alignment-X #center
                \sustainOff
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#blue"
        >>> abjad.tweak(start_piano_pedal).parent_alignment_X = abjad.Center
        >>> abjad.attach(start_piano_pedal, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal(leak=True)
        >>> abjad.tweak(stop_piano_pedal).color = "#red"
        >>> abjad.tweak(stop_piano_pedal).parent_alignment_X = abjad.Center
        >>> abjad.attach(stop_piano_pedal, staff[-2])
        >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = 5
            }
            {
                c'4
                - \tweak color #blue
                - \tweak parent-alignment-X #center
                \sustainOn
                d'4
                e'4
                <>
                - \tweak color #red
                - \tweak parent-alignment-X #center
                \sustainOff
                r4
            }

    ..  container:: example

        REGRESSION. Tweaks survive copy:

        >>> import copy
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.tweak(stop_piano_pedal).color = "#blue"
        >>> stop_piano_pedal
        StopPianoPedal(kind=None, leak=False, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

        >>> stop_piano_pedal_2 = copy.copy(stop_piano_pedal)
        >>> stop_piano_pedal_2
        StopPianoPedal(kind=None, leak=False, tweaks=TweakInterface(('_literal', False), ('color', '#blue')))

    """

    kind: str | None = None
    leak: bool = False
    tweaks: _overrides.TweakInterface | None = None

    _is_dataclass = True
    context = "StaffGroup"
    parameter = "PEDAL"
    persistent = True
    spanner_stop = True

    _time_orientation = _enums.Right

    def __post_init__(self):
        if self.kind is not None:
            assert self.kind in ("sustain", "sostenuto", "corda")
        if self.leak is not None:
            self.leak = bool(self.leak)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        strings = []
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            strings.extend(tweaks)
            # bundle.after.spanner_stops.extend(tweaks)
        if self.kind == "corda":
            string = r"\treCorde"
        elif self.kind == "sostenuto":
            string = r"\sostenutoOff"
        else:
            assert self.kind in ("sustain", None)
            string = r"\sustainOff"
        strings.append(string)
        if self.leak:
            strings.insert(0, "<>")
            bundle.after.leaks.extend(strings)
        else:
            bundle.after.spanner_stops.extend(strings)
        return bundle


@dataclasses.dataclass(slots=True)
class StopSlur:
    r"""
    LilyPond ``)`` command.

    ..  container:: example

        >>> abjad.StopSlur()
        StopSlur(leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartSlur()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopSlur()
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                (
                d'4
                e'4
                )
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartSlur()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopSlur(leak=True)
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                (
                d'4
                e'4
                <> )
                r4
            }

    ..  container:: example

        REGRESSION. Leaked contributions appear last in postevent format
        slot:

        >>> staff = abjad.Staff("c'8 d' e' f' r2")
        >>> abjad.beam(staff[:4])
        >>> command = abjad.StartSlur()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopSlur(leak=True)
        >>> abjad.attach(command, staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                - \tweak color #blue
                (
                d'8
                e'8
                f'8
                ]
                <> )
                r2
            }

        The leaked text spanner above does not inadvertantly leak the beam.

    """

    leak: bool = False

    _is_dataclass = True
    context = "Voice"
    parameter = "SLUR"
    persistent = True
    spanner_stop = True

    _time_orientation = _enums.Right

    def __post_init__(self):
        if self.leak is not None:
            self.leak = bool(self.leak)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = ")"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StopTextSpan:
    r"""
    LilyPond ``\stopTextSpan`` command.

    ..  container:: example

        >>> abjad.StopTextSpan()
        StopTextSpan(command='\\stopTextSpan', leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> abjad.tweak(command).staff_padding = 2.5
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopTextSpan()
        >>> abjad.attach(command, staff[-2])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> abjad.tweak(command).staff_padding = 2.5
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopTextSpan(leak=True)
        >>> abjad.attach(command, staff[-2])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                <> \stopTextSpan
                r4
            }

    """

    command: str = r"\stopTextSpan"
    leak: bool = False

    _is_dataclass = True
    context = "Voice"
    enchained = True
    parameter = "TEXT_SPANNER"
    persistent = True
    spanner_stop = True

    def __post_init__(self):
        assert isinstance(self.command, str), repr(self.command)
        assert self.command.startswith("\\"), repr(self.command)
        if self.leak is not None:
            self.leak = bool(self.leak)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = self.command
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class StopTrillSpan:
    r"""
    LilyPond ``\stopTrillSpan`` command.

    ..  container:: example

        >>> abjad.StopTrillSpan()
        StopTrillSpan(leak=False)

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartTrillSpan()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopTrillSpan()
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startTrillSpan
                d'4
                e'4
                \stopTrillSpan
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> command = abjad.StartTrillSpan()
        >>> abjad.tweak(command).color = "#blue"
        >>> abjad.attach(command, staff[0])
        >>> command = abjad.StopTrillSpan(leak=True)
        >>> abjad.attach(command, staff[-2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startTrillSpan
                d'4
                e'4
                <> \stopTrillSpan
                r4
            }

    """

    leak: bool = False

    _is_dataclass = True
    context = "Voice"
    parameter = "TRILL"
    persistent = True
    spanner_stop = True

    _time_orientation = _enums.Right

    def __post_init__(self):
        if self.leak is not None:
            self.leak = bool(self.leak)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = r"\stopTrillSpan"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle


@dataclasses.dataclass(slots=True)
class Tie:
    r"""
    LilyPond ``~`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> tie = abjad.Tie()
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ~
                c'4
                d'4
                d'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.logical_tie(leaf)
        ...
        (Note("c'4"), LogicalTie(items=[Note("c'4"), Note("c'4")]))
        (Note("c'4"), LogicalTie(items=[Note("c'4"), Note("c'4")]))
        (Note("d'4"), LogicalTie(items=[Note("d'4")]))
        (Note("d'4"), LogicalTie(items=[Note("d'4")]))


    ..  container:: example

        With ``direction`` unset:

        >>> staff = abjad.Staff("c'4 c' c'' c''")
        >>> abjad.attach(abjad.Tie(), staff[0])
        >>> abjad.attach(abjad.Tie(), staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ~
                c'4
                c''4
                ~
                c''4
            }

        With ``direction=abjad.Up``:

        >>> staff = abjad.Staff("c'4 c' c'' c''")
        >>> abjad.attach(abjad.Tie(direction=abjad.Up), staff[0])
        >>> abjad.attach(abjad.Tie(direction=abjad.Up), staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ^ ~
                c'4
                c''4
                ^ ~
                c''4
            }

        With ``direction=abjad.Down``:

        >>> staff = abjad.Staff("c'4 c' c'' c''")
        >>> abjad.attach(abjad.Tie(direction=abjad.Down), staff[0])
        >>> abjad.attach(abjad.Tie(direction=abjad.Down), staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                _ ~
                c'4
                c''4
                _ ~
                c''4
            }


    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> tie = abjad.Tie()
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ~
                c'4
                d'4
                d'4
            }

    """

    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True
    context = "Voice"
    persistent = True

    def _add_direction(self, string):
        if self.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(self.direction)
            string = f"{symbol} {string}"
        return string

    def _attachment_test_all(self, argument):
        if not (
            hasattr(argument, "written_pitch") or hasattr(argument, "written_pitches")
        ):
            string = f"Must be note or chord (not {argument})."
            return [string]
        return True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            strings = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(strings)
        string = self._add_direction("~")
        strings = [string]
        bundle.after.spanner_starts.extend(strings)
        return bundle


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class TimeSignature:
    r"""
    Time signature.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                c'8
                d'8
                e'8
            }

    ..  container:: example

        Create score-contexted time signatures like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0], context="Score")

        Score-contexted time signatures format behind comments when no Abjad score
        container is found:

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            %%% \time 3/8 %%%
            c'8
            d'8
            e'8
            c'8
            d'8
            e'8
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Score-contexted time signatures format normally when an Abjad score container is
        found:

        >>> score = abjad.Score([staff])
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new Staff
            {
                \time 3/8
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

        >>> abjad.show(score) # doctest: +SKIP

    ..  container:: example

        Time signatures can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(
        ...     time_signature,
        ...     staff[0],
        ...     context="Score",
        ...     tag=abjad.Tag("+PARTS"),
        ... )
        >>> score = abjad.Score([staff])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(score, tags=True)
        >>> print(string)
        \new Score
        <<
            \new Staff
            {
                %! +PARTS
                \time 3/8
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

    ..  container:: example

        Set ``hide=True`` time signature should not appear in output (but should still
        determine effective time signature):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> time_signature = abjad.TimeSignature((4, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> time_signature = abjad.TimeSignature((2, 4), hide=True)
        >>> abjad.attach(time_signature, staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

        >>> for leaf in abjad.iterate.leaves(staff):
        ...     prototype = abjad.TimeSignature
        ...     leaf, abjad.get.effective(leaf, prototype)
        ...
        (Note("c'4"), TimeSignature(pair=(4, 4), hide=False, partial=None))
        (Note("d'4"), TimeSignature(pair=(4, 4), hide=False, partial=None))
        (Note("e'4"), TimeSignature(pair=(2, 4), hide=True, partial=None))
        (Note("f'4"), TimeSignature(pair=(2, 4), hide=True, partial=None))

    """

    pair: tuple[int, int]
    hide: bool = False
    partial: typing.Optional[_duration.Duration] = None

    _is_dataclass = True

    _format_slot = "opening"

    # TODO: context should probably be "Score"
    context = "Staff"
    persistent = True

    def __post_init__(self):
        pair_ = getattr(self.pair, "pair", self.pair)
        assert len(pair_) == 2, repr(pair_)
        assert isinstance(pair_[0], int)
        assert isinstance(pair_[1], int)
        numerator, denominator = pair_
        self.pair = (numerator, denominator)
        if self.partial is not None:
            self.partial = _duration.Duration(self.partial)

    def __copy__(self, *arguments) -> "TimeSignature":
        """
        Copies time signature.
        """
        return type(self)((self.numerator, self.denominator), partial=self.partial)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a time signature with numerator and denominator
        equal to this time signature. Also true when ``argument`` is a tuple with first
        and second elements equal to numerator and denominator of this time signature.
        """
        if isinstance(argument, type(self)):
            if self.numerator == argument.numerator:
                if self.denominator == argument.denominator:
                    return True
        return False

    def __str__(self) -> str:
        """
        Gets string representation of time signature.

        ..  container:: example

            >>> str(abjad.TimeSignature((3, 8)))
            '3/8'

        """
        return f"{self.numerator}/{self.denominator}"

    def _get_lilypond_format(self):
        result = []
        if self.hide:
            return result
        if self.is_non_dyadic_rational:
            string = '#(ly:expect-warning "strange time signature found")'
            result.append(string)
        if self.partial is None:
            result.append(rf"\time {self.numerator}/{self.denominator}")
        else:
            duration_string = self.partial.lilypond_duration_string
            partial_directive = rf"\partial {duration_string}"
            result.append(partial_directive)
            string = rf"\time {self.numerator}/{self.denominator}"
            result.append(string)
        return result

    @property
    def denominator(self) -> int:
        """
        Gets denominator of time signature:

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).denominator
            8

        """
        return self.pair[1]

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).duration
            Duration(3, 8)

        """
        return _duration.Duration(*self.pair)

    @property
    def is_non_dyadic_rational(self) -> bool:
        r"""
        Is true when time signature has non-power-of-two denominator.

        ..  container:: example

            With non-power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((7, 12))
            >>> time_signature.is_non_dyadic_rational
            True

            With power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> time_signature.is_non_dyadic_rational
            False

            Suppresses LilyPond "strange time signature" warning:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d' e' f'")
            >>> staff = abjad.Staff([tuplet])
            >>> time_signature = abjad.TimeSignature((4, 3))
            >>> abjad.attach(time_signature, tuplet[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \times 2/3
                {
                    #(ly:expect-warning "strange time signature found")
                    \time 4/3
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }

        """
        return not _math.is_nonnegative_integer_power_of_two(self.denominator)

    @property
    def implied_prolation(self) -> _duration.Multiplier:
        """
        Gets implied prolation of time signature.

        ..  container:: example

            Implied prolation of dyadic time signature:

            >>> abjad.TimeSignature((3, 8)).implied_prolation
            Multiplier(1, 1)

            Implied prolation of nondyadic time signature:

            >>> abjad.TimeSignature((7, 12)).implied_prolation
            Multiplier(2, 3)

        """
        return _duration.Duration(1, self.denominator).implied_prolation

    @property
    def numerator(self) -> int:
        """
        Gets numerator of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).numerator
            3

        """
        return self.pair[0]

    @staticmethod
    def from_string(string) -> "TimeSignature":
        """
        Makes new time signature from fraction ``string``.

        ..  container:: example

            >>> abjad.TimeSignature.from_string("6/8")
            TimeSignature(pair=(6, 8), hide=False, partial=None)

        """
        assert isinstance(string, str), repr(string)
        parts = string.split("/")
        assert len(parts) == 2, repr(parts)
        numbers = [int(_) for _ in parts]
        numerator, denominator = numbers
        return TimeSignature((numerator, denominator))

    # TODO: remove contents_multiplier?
    # TODO: rename to to_dyadic_rational()
    def is_dyadic_rational(self, contents_multiplier=1) -> "TimeSignature":
        """
        Makes new time signature equivalent to current time signature with power-of-two
        denominator.

        ..  container:: example

            >>> abjad.TimeSignature((1, 12)).is_dyadic_rational()
            TimeSignature(pair=(1, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((2, 12)).is_dyadic_rational()
            TimeSignature(pair=(2, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((3, 12)).is_dyadic_rational()
            TimeSignature(pair=(2, 8), hide=False, partial=None)

            >>> abjad.TimeSignature((4, 12)).is_dyadic_rational()
            TimeSignature(pair=(4, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((5, 12)).is_dyadic_rational()
            TimeSignature(pair=(5, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((6, 12)).is_dyadic_rational()
            TimeSignature(pair=(4, 8), hide=False, partial=None)

            >>> abjad.TimeSignature((1, 14)).is_dyadic_rational()
            TimeSignature(pair=(1, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((2, 14)).is_dyadic_rational()
            TimeSignature(pair=(2, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((3, 14)).is_dyadic_rational()
            TimeSignature(pair=(3, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((4, 14)).is_dyadic_rational()
            TimeSignature(pair=(4, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((5, 14)).is_dyadic_rational()
            TimeSignature(pair=(5, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((6, 14)).is_dyadic_rational()
            TimeSignature(pair=(6, 14), hide=False, partial=None)

        """
        contents_multiplier = _duration.Multiplier(contents_multiplier)
        contents_multiplier = _duration.Multiplier(contents_multiplier)
        non_power_of_two_denominator = self.denominator
        if contents_multiplier == _duration.Multiplier(1):
            power_of_two_denominator = _math.greatest_power_of_two_less_equal(
                non_power_of_two_denominator
            )
        else:
            power_of_two_denominator = _math.greatest_power_of_two_less_equal(
                non_power_of_two_denominator, 1
            )
        non_dyadic_rational_pair = _duration.NonreducedFraction(self.pair)
        dyadic_rational = non_dyadic_rational_pair.with_denominator(
            power_of_two_denominator
        )
        dyadic_rational_pair = dyadic_rational.pair
        return type(self)(dyadic_rational_pair)
