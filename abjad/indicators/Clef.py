import functools
import numbers
import typing

from ..bundle import LilyPondFormatBundle
from ..pitch import _lib as pitch__lib
from ..pitch.pitches import NamedPitch
from ..storage import FormatSpecification, StorageFormatManager


class Clef:
    r"""
    Clef.

    ..  container:: example

        Some available clefs:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> clef = abjad.Clef('treble')
        >>> abjad.attach(clef, staff[0])
        >>> clef = abjad.Clef('alto')
        >>> abjad.attach(clef, staff[1])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[2])
        >>> clef = abjad.Clef('treble^8')
        >>> abjad.attach(clef, staff[3])
        >>> clef = abjad.Clef('bass_8')
        >>> abjad.attach(clef, staff[4])
        >>> clef = abjad.Clef('tenor')
        >>> abjad.attach(clef, staff[5])
        >>> clef = abjad.Clef('bass^15')
        >>> abjad.attach(clef, staff[6])
        >>> clef = abjad.Clef('percussion')
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
        ...     abjad.Clef('treble'), staff[0], tag=abjad.Tag("+PARTS")
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            \clef "treble" %! +PARTS
            c'4
            d'4
            e'4
            f'4
        }

    ..  container:: example

        LilyPond can not handle simultaneous clefs:

        >>> voice_1 = abjad.Voice("e'8 g' f' a' g' b'")
        >>> abjad.attach(abjad.Clef('treble'), voice_1[0], context='Voice')
        >>> literal = abjad.LilyPondLiteral(r"\voiceOne", "opening")
        >>> abjad.attach(literal, voice_1)
        >>> voice_1.consists_commands.append('Clef_engraver')
        >>> voice_2 = abjad.Voice("c'4. c,8 b,, a,,")
        >>> abjad.attach(abjad.Clef('treble'), voice_2[0], context='Voice')
        >>> abjad.attach(abjad.Clef('bass'), voice_2[1], context='Voice')
        >>> literal = abjad.LilyPondLiteral(r"\voiceTwo", "opening")
        >>> abjad.attach(literal, voice_2)
        >>> voice_2.consists_commands.append('Clef_engraver')
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
        >>> staff.remove_commands.append('Clef_engraver')
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

        >>> for leaf in abjad.select(voice_1).leaves():
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("e'8"), Clef('treble'))
        (Note("g'8"), Clef('treble'))
        (Note("f'8"), Clef('treble'))
        (Note("a'8"), Clef('treble'))
        (Note("g'8"), Clef('treble'))
        (Note("b'8"), Clef('treble'))

        >>> for leaf in abjad.select(voice_2).leaves():
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("c'4."), Clef('treble'))
        (Note('c,8'), Clef('bass'))
        (Note('b,,8'), Clef('bass'))
        (Note('a,,8'), Clef('bass'))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_hide", "_middle_c_position", "_name")

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

    _context = "Staff"

    _format_slot = "opening"

    _persistent = True

    _redraw = True

    _to_width = {
        "alto": 2.75,
        "varC": 2.75,
        "bass": 2.75,
        "percussion": 2.5,
        "tenor": 2.75,
        "tenorvarC": 2.75,
        "treble": 2.5,
    }

    ### INITIALIZER ###

    def __init__(self, name: str = "treble", *, hide: bool = None) -> None:
        if isinstance(name, str):
            self._name = name
        elif isinstance(name, type(self)):
            self._name = name.name
        else:
            raise TypeError("can not initialize clef: {name!r}.")
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        middle_c_position = self._calculate_middle_c_position(self._name)
        middle_c_position = StaffPosition(middle_c_position)
        self._middle_c_position = middle_c_position

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _calculate_middle_c_position(self, clef_name):
        alteration = 0
        if "_" in self._name:
            base_name, part, suffix = clef_name.partition("_")
            if suffix == "8":
                alteration = 7
            elif suffix == "15":
                alteration = 13
            else:
                raise Exception(f"bad clef alteration suffix: {suffix!r}.")
        elif "^" in self._name:
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
            "treble": NamedPitch("B4"),
            "alto": NamedPitch("C4"),
            "varC": NamedPitch("C4"),
            "tenor": NamedPitch("A3"),
            "tenorvarC": NamedPitch("A3"),
            "bass": NamedPitch("D3"),
            "french": NamedPitch("D5"),
            "soprano": NamedPitch("G4"),
            "mezzosoprano": NamedPitch("E4"),
            "baritone": NamedPitch("F3"),
            "varbaritone": NamedPitch("F3"),
            "percussion": None,
            "tab": None,
        }[clef_name]

    def _get_format_specification(self):
        return FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
        )

    def _get_lilypond_format(self):
        return rf'\clef "{self.name}"'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if not self.hide:
            bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    @classmethod
    def _list_clef_names(class_):
        return list(sorted(class_._clef_name_to_middle_c_position))

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitches(pitches) -> "Clef":
        """
        Makes clef from ``pitches``.

        ..  container:: example

            >>> maker = abjad.NoteMaker()
            >>> notes = maker(range(-12, -6), [(1, 4)])
            >>> staff = abjad.Staff(notes)
            >>> pitches = abjad.iterate(staff).pitches()
            >>> abjad.Clef.from_pitches(pitches)
            Clef('bass')

            Choses between treble and bass based on minimal number of ledger lines.

        """
        diatonic_pitch_numbers = [
            pitch._get_diatonic_pitch_number() for pitch in pitches
        ]
        max_diatonic_pitch_number = max(diatonic_pitch_numbers)
        min_diatonic_pitch_number = min(diatonic_pitch_numbers)
        lowest_treble_line_pitch = NamedPitch("E4")
        lowest_treble_line_diatonic_pitch_number = (
            lowest_treble_line_pitch._get_diatonic_pitch_number()
        )
        candidate_steps_below_treble = (
            lowest_treble_line_diatonic_pitch_number - min_diatonic_pitch_number
        )
        highest_bass_line_pitch = NamedPitch("A3")
        highest_bass_line_diatonic_pitch_number = (
            highest_bass_line_pitch._get_diatonic_pitch_number()
        )
        candidate_steps_above_bass = (
            max_diatonic_pitch_number - highest_bass_line_diatonic_pitch_number
        )
        if candidate_steps_above_bass < candidate_steps_below_treble:
            return Clef("bass")
        else:
            return Clef("treble")

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            >>> clef = abjad.Clef('treble')
            >>> clef.context
            'Staff'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def hide(self) -> typing.Optional[bool]:
        r"""
        Is true when clef should not appear in output (but should still
        determine effective clef).

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef('treble'), staff[0])
            >>> abjad.attach(abjad.Clef('alto', hide=True), staff[2])
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

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     leaf, abjad.get.effective(leaf, abjad.Clef)
            ...
            (Note("c'4"), Clef('treble'))
            (Note("d'4"), Clef('treble'))
            (Note("e'4"), Clef('alto', hide=True))
            (Note("f'4"), Clef('alto', hide=True))

        """
        return self._hide

    @property
    def middle_c_position(self) -> int:
        """
        Gets middle C position of clef.

        ..  container:: example

            Gets staff position of middle C in treble clef:

            >>> abjad.Clef('treble').middle_c_position
            StaffPosition(-6)

        ..  container:: example

            Gets staff position of middle C in alto clef:

            >>> abjad.Clef('alto').middle_c_position
            StaffPosition(0)

        """
        return self._middle_c_position

    @property
    def name(self) -> str:
        """
        Gets name of clef.

        ..  container:: example

            Gets name treble clef:

            >>> abjad.Clef('treble').name
            'treble'

        ..  container:: example

            Gets name of alto clef:

            >>> abjad.Clef('alto').name
            'alto'

        """
        return self._name

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.Clef('treble').persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def redraw(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.Clef('treble').redraw
            True

        Class constant.
        """
        return self._redraw

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on clef.

        The LilyPond ``\clef`` command refuses tweaks.

        Override the LilyPond ``Clef`` grob instead.
        """
        pass


@functools.total_ordering
class StaffPosition:
    """
    Staff position.

    ..  container:: example

        Initializes staff position at middle line of staff:

        >>> abjad.StaffPosition(0)
        StaffPosition(0)

    ..  container:: example

        Initializes staff position one space below middle line of staff:

        >>> abjad.StaffPosition(-1)
        StaffPosition(-1)

    ..  container:: example

        Initializes staff position one line below middle line of staff:

        >>> abjad.StaffPosition(-2)
        StaffPosition(-2)

    ..  container:: example

        Initializes from other staff position:

        >>> staff_position = abjad.StaffPosition(-2)
        >>> abjad.StaffPosition(staff_position)
        StaffPosition(-2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number",)

    ### INITIALIZER ###

    def __init__(self, number=0):
        if isinstance(number, type(self)):
            number = number.number
        assert isinstance(number, numbers.Number), repr(number)
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a staff position with the same number as
        this staff position.

        ..  container:: example

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

        Returns true or false.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes staff position.

        Returns integer.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __lt__(self, argument):
        """
        Is true when staff position is less than ``argument``.

        ..  container:: example

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

        Returns true or false.
        """
        try:
            argument = type(self)(argument)
        except Exception:
            return False
        return self.number < argument.number

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of staff position.

        ..  container:: example

            >>> str(abjad.StaffPosition(-2))
            'StaffPosition(-2)'

        Returns string.
        """
        return f"{type(self).__name__}({self.number})"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.number],
            storage_format_keyword_names=[],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        """
        Gets staff position number.

        ..  container:: example

            >>> abjad.StaffPosition(-2).number
            -2

        Returns number.
        """
        return self._number

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_and_clef(pitch, clef) -> "StaffPosition":
        r"""
        Changes named pitch to staff position.

        ..  container:: example

            Changes C#5 to absolute staff position:

            >>> abjad.StaffPosition.from_pitch_and_clef('C#5', "alto")
            StaffPosition(7)

            >>> abjad.StaffPosition.from_pitch_and_clef('C#5', "treble")
            StaffPosition(1)

            >>> abjad.StaffPosition.from_pitch_and_clef('C#5', "bass")
            StaffPosition(13)

        ..  container:: example

            Marks up absolute staff position of many pitches:

            >>> string = "g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''"
            >>> staff = abjad.Staff(string)
            >>> for note in staff:
            ...     staff_position = abjad.StaffPosition.from_pitch_and_clef(
            ...         note.written_pitch,
            ...         "alto",
            ...     )
            ...     markup = abjad.Markup(staff_position.number)
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
                    - \markup { -3 }
                    a16
                    - \markup { -2 }
                    b16
                    - \markup { -1 }
                    c'16
                    - \markup { 0 }
                    d'16
                    - \markup { 1 }
                    e'16
                    - \markup { 2 }
                    f'16
                    - \markup { 3 }
                    g'16
                    - \markup { 4 }
                    a'16
                    - \markup { 5 }
                    b'16
                    - \markup { 6 }
                    c''16
                    - \markup { 7 }
                    d''16
                    - \markup { 8 }
                    e''16
                    - \markup { 9 }
                    f''16
                    - \markup { 10 }
                    g''16
                    - \markup { 11 }
                    a''16
                    - \markup { 12 }
                }

        ..  container:: example

            Marks up bass staff position of many pitches:

            >>> string = "g,16 a, b, c d e f g a b c' d' e' f' g' a'"
            >>> staff = abjad.Staff(string)
            >>> for note in staff:
            ...     staff_position = abjad.StaffPosition.from_pitch_and_clef(
            ...         note.written_pitch,
            ...         "bass",
            ...     )
            ...     markup = abjad.Markup(staff_position.number)
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
                    - \markup { -4 }
                    a,16
                    - \markup { -3 }
                    b,16
                    - \markup { -2 }
                    c16
                    - \markup { -1 }
                    d16
                    - \markup { 0 }
                    e16
                    - \markup { 1 }
                    f16
                    - \markup { 2 }
                    g16
                    - \markup { 3 }
                    a16
                    - \markup { 4 }
                    b16
                    - \markup { 5 }
                    c'16
                    - \markup { 6 }
                    d'16
                    - \markup { 7 }
                    e'16
                    - \markup { 8 }
                    f'16
                    - \markup { 9 }
                    g'16
                    - \markup { 10 }
                    a'16
                    - \markup { 11 }
                }

        """
        pitch = NamedPitch(pitch)
        clef = Clef(clef)
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
            ...     pitch = staff_position.to_pitch("treble")
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(-6)    c'
            StaffPosition(-5)    d'
            StaffPosition(-4)    e'
            StaffPosition(-3)    f'
            StaffPosition(-2)    g'
            StaffPosition(-1)    a'
            StaffPosition(0)    b'
            StaffPosition(1)    c''
            StaffPosition(2)    d''
            StaffPosition(3)    e''
            StaffPosition(4)    f''
            StaffPosition(5)    g''

        ..  container:: example

            Bass clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch("bass")
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(-6)    e,
            StaffPosition(-5)    f,
            StaffPosition(-4)    g,
            StaffPosition(-3)    a,
            StaffPosition(-2)    b,
            StaffPosition(-1)    c
            StaffPosition(0)    d
            StaffPosition(1)    e
            StaffPosition(2)    f
            StaffPosition(3)    g
            StaffPosition(4)    a
            StaffPosition(5)    b

        ..  container:: example

            Alto clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch("alto")
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(-6)    d
            StaffPosition(-5)    e
            StaffPosition(-4)    f
            StaffPosition(-3)    g
            StaffPosition(-2)    a
            StaffPosition(-1)    b
            StaffPosition(0)    c'
            StaffPosition(1)    d'
            StaffPosition(2)    e'
            StaffPosition(3)    f'
            StaffPosition(4)    g'
            StaffPosition(5)    a'

        ..  container:: example

            Percussion clef:

            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = staff_position.to_pitch("percussion")
            ...     message = f"{staff_position!s}    {pitch}"
            ...     print(message)
            ...
            StaffPosition(-6)    d
            StaffPosition(-5)    e
            StaffPosition(-4)    f
            StaffPosition(-3)    g
            StaffPosition(-2)    a
            StaffPosition(-1)    b
            StaffPosition(0)    c'
            StaffPosition(1)    d'
            StaffPosition(2)    e'
            StaffPosition(3)    f'
            StaffPosition(4)    g'
            StaffPosition(5)    a'

        Returns new named pitch.
        """
        offset_staff_position_number = self.number
        clef = Clef(clef)
        offset_staff_position_number -= clef.middle_c_position.number
        offset_staff_position = StaffPosition(offset_staff_position_number)
        octave_number = offset_staff_position.number // 7 + 4
        diatonic_pc_number = offset_staff_position.number % 7
        pitch_class_number = pitch__lib._diatonic_pc_number_to_pitch_class_number[
            diatonic_pc_number
        ]
        pitch_number = 12 * (octave_number - 4)
        pitch_number += pitch_class_number
        named_pitch = NamedPitch(pitch_number)
        return named_pitch
