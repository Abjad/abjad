"""
Indicators.
"""
import collections
import dataclasses
import fractions
import functools
import math
import typing

from . import contributions as _contributions
from . import duration as _duration
from . import enums as _enums
from . import math as _math
from . import overrides as _overrides
from . import pitch as _pitch
from . import sequence as _sequence
from . import string as _string

_EMPTY_CHORD = "<>"


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> arpeggio = abjad.Arpeggio(direction=abjad.DOWN)
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
        >>> bundle = abjad.bundle(arpeggio, r"- \tweak color #blue")
        >>> abjad.attach(bundle, chord)
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

    direction: _enums.Vertical | None = None

    post_event: typing.ClassVar[bool] = True

    def __post_init__(self):
        if self.direction is not None:
            assert isinstance(self.direction, _enums.Vertical), repr(self.direction)

    def _get_lilypond_format(self):
        return r"\arpeggio"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        contributions.after.articulations.append(r"\arpeggio")
        if self.direction in (_enums.UP, _enums.DOWN):
            if self.direction is _enums.UP:
                command = r"\arpeggioArrowUp"
            else:
                command = r"\arpeggioArrowDown"
            contributions.before.commands.append(command)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Articulation:
    r"""
    Articulation.

    ..  container:: example

        >>> abjad.Articulation("staccato")
        Articulation(name='staccato')

        >>> abjad.Articulation(".")
        Articulation(name='.')

        Use ``direction=abjad.UP`` like this:

        >>> note = abjad.Note("c'4")
        >>> articulation = abjad.Articulation("staccato")
        >>> abjad.attach(articulation, note, direction=abjad.UP)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            ^ \staccato

        Use ``direction=abjad.DOWN`` like this:

        >>> note = abjad.Note("c'4")
        >>> articulation = abjad.Articulation("staccato")
        >>> abjad.attach(articulation, note, direction=abjad.DOWN)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            _ \staccato

        Use ``dataclasses.replace()`` like this:

        >>> import dataclasses
        >>> articulation = abjad.Articulation(".")
        >>> dataclasses.replace(articulation)
        Articulation(name='.')

    """

    name: str

    post_event: typing.ClassVar[bool] = True
    shortcut_to_word: typing.ClassVar[dict[str, str]] = {
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

    def _get_lilypond_format(self, wrapper=None):
        if self.name:
            string = self.shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if wrapper is not None and wrapper.direction:
                direction_ = _string.to_tridirectional_lilypond_symbol(
                    wrapper.direction
                )
                direction = direction_
            else:
                direction = "-"
            return rf"{direction} \{string}"
        else:
            return ""

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format(wrapper=wrapper)
        contributions.after.articulations.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BarLine:
    r"""
    Bar line.

    ..  container:: example

        Final bar line:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> bar_line = abjad.BarLine("|.")
        >>> abjad.attach(bar_line, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|."
                }
            >>

    ..  container:: example

        Specify repeat bars like this:

        >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''", name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.BarLine(".|:"), staff[3])
        >>> abjad.attach(abjad.BarLine(":|."), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
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
            >>

        This allows you to bypass LilyPond's ``\volta`` command.

    """

    abbreviation: str = "|"
    site: str = "after"

    context: typing.ClassVar[str] = "Score"
    # find_context_on_attach: typing.ClassVar[bool] = True
    known_abbreviations: typing.ClassVar[tuple[str, ...]] = (
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

    def __post_init__(self):
        """
        LilyPond fails to error on unknown bar-line abbreviation, so we check here.
        """
        if self.abbreviation not in self.known_abbreviations:
            raise Exception(f"unknown bar-line abbreviation: {self.abbreviation!r}.")

    def _get_lilypond_format(self):
        return rf'\bar "{self.abbreviation}"'

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        site = getattr(contributions, self.site)
        site.commands.append(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BeamCount:
    r"""
    LilyPond ``\setLeftBeamCount``, ``\setRightBeamCount`` command.

    ..  container:: example

        >>> abjad.BeamCount()
        BeamCount(left=0, right=0)

    """

    left: int = 0
    right: int = 0

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = rf"\set stemLeftBeamCount = {self.left}"
        contributions.before.commands.append(string)
        string = rf"\set stemRightBeamCount = {self.right}"
        contributions.before.commands.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> bundle = abjad.bundle(bend_after, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

    bend_amount: int | float = -4

    post_event: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "after"
    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT

    def _get_lilypond_format(self):
        return rf"- \bendAfter #'{self.bend_amount}"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format()
        contributions.after.articulations.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BreathMark:
    r"""
    Breath mark.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d' e' f' g' a' b' c''")
        >>> staff = abjad.Staff([voice])
        >>> abjad.beam(voice[:4])
        >>> abjad.beam(voice[4:])
        >>> abjad.attach(abjad.BreathMark(), voice[3])
        >>> abjad.attach(abjad.BreathMark(), voice[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
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

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> breath = abjad.BreathMark()
        >>> bundle = abjad.bundle(breath, r"\tweak color #blue")
        >>> abjad.attach(bundle, note)
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

    site: typing.ClassVar[str] = "after"
    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT

    def _before_attach(self, deactivate, component):
        for indicator in component._get_indicators():
            if isinstance(indicator, type(self)) and indicator.site == self.site:
                classname = type(component).__name__
                message = f"can not attach {self!r} to {classname}:"
                message += f"\n    {indicator!r} is already attached to {classname}."
                raise Exception(message)

    def _get_lilypond_format(self):
        return r"\breathe"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format()
        contributions.after.commands.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> voice_2 = abjad.Voice("c'4. c,8 b,, a,,")
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
        >>> abjad.attach(abjad.Clef("treble"), voice_1[0], context="Voice")
        >>> command = abjad.VoiceNumber(1)
        >>> abjad.attach(command, voice_1[0])
        >>> voice_1.consists_commands.append("Clef_engraver")
        >>> abjad.attach(abjad.Clef("treble"), voice_2[0], context="Voice")
        >>> abjad.attach(abjad.Clef("bass"), voice_2[1], context="Voice")
        >>> command = abjad.VoiceNumber(2)
        >>> abjad.attach(command, voice_2[0])
        >>> voice_2.consists_commands.append("Clef_engraver")
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

        >>> abjad.Clef("treble").middle_c_position()
        StaffPosition(number=-6)

        >>> abjad.Clef("alto").middle_c_position()
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
    hide: bool = dataclasses.field(compare=False, default=False)

    context: typing.ClassVar[str] = "Staff"
    # find_context_on_attach: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    redraw: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "before"

    clef_name_to_middle_c_position = {
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
        assert isinstance(self.hide, bool), repr(self.hide)

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
        return self.clef_name_to_middle_c_position[base_name] + alteration

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

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        if not self.hide:
            contributions.opening.commands.append(self._get_lilypond_format())
        return contributions

    @classmethod
    def from_pitches(class_, pitches) -> "Clef":
        """
        Makes clef from ``pitches``.

        ..  container:: example

            >>> notes = abjad.makers.make_notes(list(range(-12, -6)), [(1, 4)])
            >>> staff = abjad.Staff(notes)
            >>> pitches = abjad.iterate.pitches(staff)
            >>> abjad.Clef.from_pitches(pitches)
            Clef(name='bass', hide=False)

            Chooses between treble and bass based on minimal number of ledger lines.

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

    def middle_c_position(self):
        """
        Gets middle C position.
        """
        middle_c_position = self._calculate_middle_c_position(self.name)
        middle_c_position = _pitch.StaffPosition(middle_c_position)
        return middle_c_position

    def to_pitch(self, staff_position) -> _pitch.NamedPitch:
        """
        Changes ``staff_position`` to pitch.

        Treble clef:

        ..  container:: example

            >>> clef = abjad.Clef("treble")
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = clef.to_pitch(staff_position)
            ...     print(f"{staff_position!r:25}{pitch!r}")
            ...
            StaffPosition(number=-6) NamedPitch("c'")
            StaffPosition(number=-5) NamedPitch("d'")
            StaffPosition(number=-4) NamedPitch("e'")
            StaffPosition(number=-3) NamedPitch("f'")
            StaffPosition(number=-2) NamedPitch("g'")
            StaffPosition(number=-1) NamedPitch("a'")
            StaffPosition(number=0)  NamedPitch("b'")
            StaffPosition(number=1)  NamedPitch("c''")
            StaffPosition(number=2)  NamedPitch("d''")
            StaffPosition(number=3)  NamedPitch("e''")
            StaffPosition(number=4)  NamedPitch("f''")
            StaffPosition(number=5)  NamedPitch("g''")

        ..  container:: example

            Bass clef:

            >>> clef = abjad.Clef("bass")
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = clef.to_pitch(staff_position)
            ...     print(f"{staff_position!r:25}{pitch!r}")
            ...
            StaffPosition(number=-6) NamedPitch('e,')
            StaffPosition(number=-5) NamedPitch('f,')
            StaffPosition(number=-4) NamedPitch('g,')
            StaffPosition(number=-3) NamedPitch('a,')
            StaffPosition(number=-2) NamedPitch('b,')
            StaffPosition(number=-1) NamedPitch('c')
            StaffPosition(number=0)  NamedPitch('d')
            StaffPosition(number=1)  NamedPitch('e')
            StaffPosition(number=2)  NamedPitch('f')
            StaffPosition(number=3)  NamedPitch('g')
            StaffPosition(number=4)  NamedPitch('a')
            StaffPosition(number=5)  NamedPitch('b')

        ..  container:: example

            Alto clef:

            >>> clef = abjad.Clef("alto")
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = clef.to_pitch(staff_position)
            ...     print(f"{staff_position!r:25}{pitch!r}")
            ...
            StaffPosition(number=-6) NamedPitch('d')
            StaffPosition(number=-5) NamedPitch('e')
            StaffPosition(number=-4) NamedPitch('f')
            StaffPosition(number=-3) NamedPitch('g')
            StaffPosition(number=-2) NamedPitch('a')
            StaffPosition(number=-1) NamedPitch('b')
            StaffPosition(number=0)  NamedPitch("c'")
            StaffPosition(number=1)  NamedPitch("d'")
            StaffPosition(number=2)  NamedPitch("e'")
            StaffPosition(number=3)  NamedPitch("f'")
            StaffPosition(number=4)  NamedPitch("g'")
            StaffPosition(number=5)  NamedPitch("a'")

        ..  container:: example

            Percussion clef:

            >>> clef = abjad.Clef("percussion")
            >>> for n in range(-6, 6):
            ...     staff_position = abjad.StaffPosition(n)
            ...     pitch = clef.to_pitch(staff_position)
            ...     print(f"{staff_position!r:25}{pitch!r}")
            ...
            StaffPosition(number=-6) NamedPitch('d')
            StaffPosition(number=-5) NamedPitch('e')
            StaffPosition(number=-4) NamedPitch('f')
            StaffPosition(number=-3) NamedPitch('g')
            StaffPosition(number=-2) NamedPitch('a')
            StaffPosition(number=-1) NamedPitch('b')
            StaffPosition(number=0)  NamedPitch("c'")
            StaffPosition(number=1)  NamedPitch("d'")
            StaffPosition(number=2)  NamedPitch("e'")
            StaffPosition(number=3)  NamedPitch("f'")
            StaffPosition(number=4)  NamedPitch("g'")
            StaffPosition(number=5)  NamedPitch("a'")

        """
        assert isinstance(staff_position, _pitch.StaffPosition), repr(staff_position)
        offset_staff_position_number = staff_position.number
        offset_staff_position_number -= self.middle_c_position().number
        offset_staff_position = _pitch.StaffPosition(offset_staff_position_number)
        octave_number = offset_staff_position.number // 7 + 4
        diatonic_pc_number = offset_staff_position.number % 7
        pitch_class_number = _pitch._diatonic_pc_number_to_pitch_class_number[
            diatonic_pc_number
        ]
        pitch_number = 12 * (octave_number - 4)
        pitch_number += pitch_class_number
        named_pitch = _pitch.NamedPitch(pitch_number)
        return named_pitch

    def to_staff_position(self, pitch) -> _pitch.StaffPosition:
        r"""
        Changes ``pitch`` to staff position.

        Changes C#5 to absolute staff position:

        ..  container:: example

            >>> pitch = abjad.NamedPitch("C#5")

            >>> abjad.Clef("alto").to_staff_position(pitch)
            StaffPosition(number=7)

            >>> abjad.Clef("treble").to_staff_position(pitch)
            StaffPosition(number=1)

            >>> abjad.Clef("bass").to_staff_position(pitch)
            StaffPosition(number=13)

        ..  container:: example

            Labels absolute staff position:

            >>> string = "g16 a b c' d' e' f' g' a' b' c'' d'' e'' f'' g'' a''"
            >>> staff = abjad.Staff(string)
            >>> clef = abjad.Clef("alto")
            >>> for note in staff:
            ...     staff_position = clef.to_staff_position(note.written_pitch)
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

            Labels staff position in bass clef:

            >>> string = "g,16 a, b, c d e f g a b c' d' e' f' g' a'"
            >>> staff = abjad.Staff(string)
            >>> clef = abjad.Clef("bass")
            >>> for note in staff:
            ...     staff_position = clef.to_staff_position(note.written_pitch)
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
        assert isinstance(pitch, _pitch.NamedPitch)
        staff_position_number = pitch._get_diatonic_pitch_number()
        staff_position_number += self.middle_c_position().number
        staff_position = _pitch.StaffPosition(staff_position_number)
        return staff_position


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ColorFingering:
    r"""
    Color fingering.

    ..  container:: example

        >>> fingering = abjad.ColorFingering(1)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note, direction=abjad.UP)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> fingering = abjad.ColorFingering(1)
        >>> bundle = abjad.bundle(fingering, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0], direction=abjad.UP)
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

    Color fingerings indicate alternate woodwind fingerings by amount of pitch of timbre
    deviation.

    """

    number: int

    directed: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "after"

    def __post_init__(self):
        assert isinstance(self.number, int), repr(self.number)

    def _get_lilypond_format(self):
        return self.markup._get_lilypond_format()

    def _get_contributions(self, *, component=None, wrapper=None):
        return self.markup._get_contributions(component=component, wrapper=wrapper)

    @property
    def markup(self) -> typing.Optional["Markup"]:
        r"""
        Gets markup of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> string = abjad.lilypond(fingering.markup)
            >>> print(string)
            \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }

        """
        if self.number is None:
            return None
        string = rf"\override #'(circle-padding . 0.25) \circle \finger {self.number}"
        string = rf"\markup {{ {string} }}"
        markup = Markup(string)
        return markup


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> staff = abjad.Staff([note], name="Staff")
        >>> score = abjad.Score([staff], name="Score")
        >>> fermata = abjad.Fermata()
        >>> bundle = abjad.bundle(fermata, r"- \tweak color #blue")
        >>> abjad.attach(bundle, note)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \fermata

    """

    command: str = "fermata"

    allowable_commands: typing.ClassVar = (
        "fermata",
        "longfermata",
        "shortfermata",
        "verylongfermata",
    )
    context: typing.ClassVar[str] = "Score"
    # find_context_on_attach: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "after"

    def __post_init__(self):
        assert self.command in self.allowable_commands, repr(self.command)

    def _get_lilypond_format(self):
        return rf"\{self.command}"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        contributions.after.articulations.append(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Glissando:
    r"""
    LilyPond ``\glissando`` command.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 d' e' f'", name="Voice")
        >>> glissando = abjad.Glissando()
        >>> bundle = abjad.bundle(glissando, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'4
                - \tweak color #blue
                \glissando
                d'4
                e'4
                f'4
            }

    """

    zero_padding: bool = False

    context: typing.ClassVar[str] = "Voice"
    # find_context_on_attach: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.zero_padding, bool), repr(self.zero_padding)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        strings = []
        if self.zero_padding:
            strings.append(r"- \abjad-zero-padding-glissando")
        strings.append(r"\glissando")
        contributions.after.spanner_starts.extend(strings)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class InstrumentName:
    r"""
    LilyPond ``\instrumentName`` setting.

    ..  container:: example

        Set instrument name to markup like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> markup = abjad.Markup(r"\markup Cellos")
        >>> instrument_name = abjad.InstrumentName(markup)
        >>> abjad.attach(instrument_name, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set Staff.instrumentName = \markup Cellos
                c'4
                d'4
                e'4
                f'4
            }

        Set instrument name to custom-defined function like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> instrument_name = abjad.InstrumentName(r"\my_instrument_name")
        >>> abjad.attach(instrument_name, staff[0])

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

        >>> name_1 = abjad.InstrumentName(r"\markup Harp", context="PianoStaff")
        >>> name_2 = abjad.InstrumentName(r"\markup Harp", context="PianoStaff")
        >>> name_3 = abjad.InstrumentName(r"\markup Harp", context="Staff")

        >>> name_1 == name_1
        True
        >>> name_1 == name_2
        True
        >>> name_1 == name_3
        False

        >>> name_2 == name_1
        True
        >>> name_2 == name_2
        True
        >>> name_2 == name_3
        False

        >>> name_3 == name_1
        False
        >>> name_3 == name_2
        False
        >>> name_3 == name_3
        True

    """

    markup: typing.Union[str, "Markup"]
    _: dataclasses.KW_ONLY
    context: str = "Staff"

    # find_context_on_attach: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "before"

    def __post_init__(self):
        assert isinstance(self.markup, str | Markup), repr(self.markup)
        assert isinstance(self.context, str), repr(self.context)

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
        if isinstance(self.markup, Markup):
            string = self.markup.string
        else:
            assert isinstance(self.markup, str)
            string = self.markup
        string = rf"\set {context!s}.instrumentName = {string}"
        result.append(string)
        return result

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        site = getattr(contributions, self.site)
        site.commands.extend(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class KeyCluster:
    r"""
    Key cluster.

    ..  container:: example

        Includes flat markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_flat_markup=True)
        >>> abjad.attach(key_cluster, chord, direction=abjad.UP)
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

        Includes natural markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_natural_markup=True)
        >>> abjad.attach(key_cluster, chord, direction=abjad.UP)
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

        Key cluster output includes overrides instead of tweaks:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster()
        >>> abjad.attach(key_cluster, chord, direction=abjad.UP)
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

    """

    include_flat_markup: bool = True
    include_natural_markup: bool = True

    directed: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.include_flat_markup, bool), repr(
            self.include_flat_markup
        )
        assert isinstance(self.include_natural_markup, bool), repr(
            self.include_natural_markup
        )

    def _get_contributions(self, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        contributions.grob_overrides.append(
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
        string = rf"\markup {string}"
        if wrapper.direction is _enums.UP:
            string = rf"^ {string}"
        elif wrapper.direction is _enums.DOWN:
            string = rf"_ {string}"
        contributions.after.markup.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LilyPondLiteral:
    r"""
    LilyPond literal.

    ..  container:: example

        Dotted slur:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r"\slurDotted", site="before")
        >>> abjad.attach(literal, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
            }

    ..  container:: example

        Use the absolute before and absolute after format sites like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r"\slurDotted", site="before")
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral("", site="absolute_before")
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral(
        ...     "% before all formatting",
        ...     site="absolute_before",
        ... )
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral("", site="absolute_after")
        >>> abjad.attach(literal, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
            <BLANKLINE>
                % before all formatting
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
            <BLANKLINE>
            }

    ..  container:: example

        LilyPond literals can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r"\slurDotted", site="before")
        >>> abjad.attach(literal, staff[0], tag=abjad.Tag("+PARTS"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            %! +PARTS
            \slurDotted
            c'8
            (
            d'8
            e'8
            f'8
            )
        }

    ..  container:: example

        Multiline input is allowed:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> lines = [
        ...     r"\stopStaff",
        ...     r"\startStaff",
        ...     r"\once \override Staff.StaffSymbol.color = #red",
        ... ]
        >>> literal = abjad.LilyPondLiteral(lines, site="before")
        >>> abjad.attach(literal, staff[2], tag=abjad.Tag("+PARTS"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'8
            (
            d'8
            %! +PARTS
            \stopStaff
            %! +PARTS
            \startStaff
            %! +PARTS
            \once \override Staff.StaffSymbol.color = #red
            e'8
            f'8
            )
        }

    ..  container:: example

        REGRESSION. Duplicate literals are allowed:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> literal = abjad.LilyPondLiteral("% text", site="before")
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral("% text", site="before")
        >>> abjad.attach(literal, staff[0])

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            % text
            % text
            c'4
            d'4
            e'4
            f'4
        }

    ..  container:: example

        Directed literal:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> literal = abjad.LilyPondLiteral(r"\f", directed=True, site="after")
        >>> bundle = abjad.bundle(
        ...     literal,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak DynamicLineSpanner.staff-padding 5",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak DynamicLineSpanner.staff-padding 5
                - \tweak color #blue
                \f
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Nondirected literal:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> literal = abjad.LilyPondLiteral(
        ...     r"\breathe",
        ...     directed=False,
        ...     site="after",
        ... )
        >>> bundle = abjad.bundle(literal, r"\tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \tweak color #blue
                \breathe
                d'4
                e'4
                f'4
            }

        Proper use of the ``directed`` property entails searching the LilyPond
        docs to understand whether LilyPond treats any particular command as
        directed or not. Most LilyPond commands are directed. LilyPond insists
        that a few commands (include ``\breathe``, ``\key``, ``\mark``) must
        not be directed.

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> literal = abjad.LilyPondLiteral(r"\f", directed=True, site="after")
        >>> bundle = abjad.bundle(literal, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \f
                d'4
                e'4
                f'4
            }

    """

    argument: str | list[str] = ""
    _: dataclasses.KW_ONLY
    site: str = "before"
    directed: bool = False

    allowable_sites: typing.ClassVar[tuple[str, ...]] = (
        "absolute_after",
        "absolute_before",
        "after",
        "before",
        "closing",
        "opening",
    )
    can_attach_to_containers: typing.ClassVar[bool] = True
    format_leaf_children: typing.ClassVar[bool] = False

    def __post_init__(self):
        if not isinstance(self.argument, str):
            assert all(isinstance(_, str) for _ in self.argument), repr(self.argument)
        assert isinstance(self.directed, bool), repr(self.directed)
        assert isinstance(self.site, str), repr(self.site)
        assert self.site in self.allowable_sites, repr(self.site)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        site = getattr(contributions, self.site)
        if isinstance(self.argument, str):
            pieces = [self.argument]
        else:
            assert isinstance(self.argument, list)
            pieces = self.argument[:]
        site.commands.extend(pieces)
        return contributions

    @property
    def post_event(self):
        """
        Is true when literal is directed.
        """
        return self.directed


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Mode:
    """
    Mode.

    ..  container:: example

        >>> abjad.Mode("major")
        Mode(name='major')

    """

    name: str = "major"

    def __post_init__(self):
        assert isinstance(self.name, str), repr(self.name)

    def intervals(self):
        """
        Gets intervals in mode.

        ..  container:: example

            >>> for _ in abjad.Mode("major").intervals(): _
            NamedInterval('+M2')
            NamedInterval('+M2')
            NamedInterval('+m2')
            NamedInterval('+M2')
            NamedInterval('+M2')
            NamedInterval('+M2')
            NamedInterval('+m2')

            >>> for _ in abjad.Mode("dorian").intervals(): _
            NamedInterval('+M2')
            NamedInterval('+m2')
            NamedInterval('+M2')
            NamedInterval('+M2')
            NamedInterval('+M2')
            NamedInterval('+m2')
            NamedInterval('+M2')

        """
        intervals = []
        m2 = _pitch.NamedInterval("m2")
        M2 = _pitch.NamedInterval("M2")
        A2 = _pitch.NamedInterval("aug2")
        dorian = [M2, m2, M2, M2, M2, m2, M2]
        if self.name == "dorian":
            intervals.extend(_sequence.rotate(dorian, n=0))
        elif self.name == "phrygian":
            intervals.extend(_sequence.rotate(dorian, n=-1))
        elif self.name == "lydian":
            intervals.extend(_sequence.rotate(dorian, n=-2))
        elif self.name == "mixolydian":
            intervals.extend(_sequence.rotate(dorian, n=-3))
        elif self.name in ("aeolian", "minor", "natural minor"):
            intervals.extend(_sequence.rotate(dorian, n=-4))
        elif self.name == "locrian":
            intervals.extend(_sequence.rotate(dorian, n=-5))
        elif self.name in ("ionian", "major"):
            intervals.extend(_sequence.rotate(dorian, n=-6))
        elif self.name == "melodic minor":
            intervals.extend([M2, m2, M2, M2, M2, M2, m2])
        elif self.name == "harmonic minor":
            intervals.extend([M2, m2, M2, M2, m2, A2, m2])
        else:
            raise ValueError(f"unknown mode name: {self.name!r}.")
        return intervals


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class KeySignature:
    r"""
    Key signature.

    ..  container:: example

        >>> staff = abjad.Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = abjad.KeySignature(
        ...     abjad.NamedPitchClass("e"), abjad.Mode("major")
        ... )
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
        >>> key_signature = abjad.KeySignature(
        ...     abjad.NamedPitchClass("e"), abjad.Mode("minor")
        ... )
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
        >>> key_signature = abjad.KeySignature(
        ...     abjad.NamedPitchClass("e"), abjad.Mode("minor")
        ... )
        >>> bundle = abjad.bundle(key_signature, r"\tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

    context: typing.ClassVar[str] = "Staff"
    # find_context_on_attach: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    redraw: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.tonic, _pitch.NamedPitchClass), repr(self.tonic)
        assert isinstance(self.mode, Mode), repr(self.mod)

    def _get_lilypond_format(self):
        assert isinstance(self.mode, Mode), repr(self.mode)
        return rf"\key {self.tonic.name} \{self.mode.name}"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format()
        contributions.before.commands.append(string)
        return contributions

    @property
    def name(self) -> str:
        """
        Gets name of key signature.

        ..  container:: example

            >>> abjad.KeySignature(abjad.NamedPitchClass("e"), abjad.Mode("major")).name
            'E major'

            >>> abjad.KeySignature(abjad.NamedPitchClass("e"), abjad.Mode("minor")).name
            'e minor'

        """
        assert isinstance(self.mode, Mode)
        if self.mode.name == "major":
            tonic = self.tonic.name.upper()
        else:
            tonic = self.tonic.name
        return f"{tonic!s} {self.mode.name}"


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> bundle = abjad.bundle(lv, r"- \tweak color #blue")
        >>> abjad.attach(bundle, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \laissezVibrer

    """

    post_event: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "after"
    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT

    def _get_lilypond_format(self):
        return r"\laissezVibrer"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        contributions.after.articulations.append(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Markup:
    r"""
    LilyPond markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> markup = abjad.Markup(r'\markup \italic "Allegro assai"')
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                ^ \markup \italic "Allegro assai"
                d'8
                e'8
                f'8
            }

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r'\markup \bold "Allegro assai"')
        >>> bundle = abjad.bundle(markup, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ^ \markup \bold "Allegro assai"
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Markup can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup \italic Allegro")
        >>> abjad.attach(markup, staff[0], direction=abjad.UP, tag=abjad.Tag("RED:M1"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! M1
            %! RED
            ^ \markup \italic Allegro
            d'4
            e'4
            f'4
        }

        Tagged markup can be deactivated:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup \italic Allegro")
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     direction=abjad.UP,
        ...     tag=abjad.Tag("RED:M1"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! M1
            %! RED
            %@% ^ \markup \italic Allegro
            d'4
            e'4
            f'4
        }

    ..  container:: example

        REGRESSION: markup 1 doesn't disappear after markup 2 is attached:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup(r"\markup \italic Allegro")
        >>> markup_2 = abjad.Markup(r'\markup \italic "non troppo"')
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP)
        >>> abjad.attach(markup_2, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ^ \markup \italic "non troppo"
                ^ \markup \italic Allegro
                d'4
                e'4
                f'4
            }

    """

    string: str

    directed: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.string, str), repr(self.string)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format(wrapper=wrapper)
        contributions.after.markup.append(string)
        return contributions

    def _get_lilypond_format(self, *, wrapper=None):
        string = self.string
        if wrapper:
            direction = wrapper.direction or "-"
            direction = _string.to_tridirectional_lilypond_symbol(direction)
            string = rf"{direction} {self.string}"
        return string


@functools.total_ordering
@dataclasses.dataclass(frozen=True, slots=True, unsafe_hash=True)
class MetronomeMark:
    r"""
    MetronomeMark.

    ..  container:: example

        Initializes integer-valued metronome mark:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 90)
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

        >>> import fractions
        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), fractions.Fraction(272, 3))
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
        ...     abjad.Duration(1, 4),
        ...     fractions.Fraction(272, 3),
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
        ...     abjad.Duration(1, 4),
        ...     fractions.Fraction(901, 10),
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
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), (120, 133), "Quick")
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

        >>> import fractions
        >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
        ...     abjad.Duration(1, 4),
        ...     67.5,
        ...  )
        >>> mark = abjad.MetronomeMark(
        ...     reference_duration=abjad.Duration(1, 4),
        ...     units_per_minute=fractions.Fraction(135, 2),
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

        >>> import fractions
        >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), fractions.Fraction(272, 3))
        >>> mark.decimal
        False

        >>> mark = abjad.MetronomeMark(
        ...     abjad.Duration(1, 4), fractions.Fraction(272, 3), decimal="90.66",
        ... )
        >>> mark.decimal
        '90.66'

        >>> mark = abjad.MetronomeMark(
        ...     abjad.Duration(1, 4), fractions.Fraction(901, 10), decimal=True,
        ... )
        >>> mark.decimal
        True

    ..  container:: example

        Set ``hide=True`` when metronome mark should not appear in output (but
        should still determine effective metronome mark):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> metronome_mark_1 = abjad.MetronomeMark(abjad.Duration(1, 4), 72)
        >>> abjad.attach(metronome_mark_1, staff[0])
        >>> metronome_mark_2 = abjad.MetronomeMark(
        ...     textual_indication="Allegro",
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

    ..  container:: example

        Equality testing:

        >>> mark_1 = abjad.MetronomeMark(abjad.Duration(3, 32), 52)
        >>> mark_2 = abjad.MetronomeMark(abjad.Duration(3, 32), 52)

        >>> mark_1 == mark_2
        True

        >>> mark_2 == mark_1
        True

    ..  container:: example

        >>> mark_1 = abjad.MetronomeMark(abjad.Duration(3, 32), 52)
        >>> mark_2 = abjad.MetronomeMark(abjad.Duration(6, 32), 104)

        >>> mark_1 == mark_2
        False

        >>> mark_2 == mark_1
        False

    ..  container:: example

        >>> mark_1 = abjad.MetronomeMark(abjad.Duration(3, 32), 52, "Langsam")
        >>> mark_2 = abjad.MetronomeMark(abjad.Duration(3, 32), 52, "Langsam")
        >>> mark_3 = abjad.MetronomeMark(abjad.Duration(3, 32), 52, "Slow")

        >>> mark_1 == mark_2
        True

        >>> mark_1 == mark_3
        False

    """

    reference_duration: _duration.Duration | None = None
    units_per_minute: int | fractions.Fraction | None = None
    textual_indication: str | None = None
    custom_markup: Markup | None = None
    decimal: bool | str = False
    hide: bool = dataclasses.field(compare=False, default=False)

    context: typing.ClassVar[str] = "Score"
    # TODO: make this work:
    # find_context_on_attach: typing.ClassVar[bool] = True
    mutates_offsets_in_seconds: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "METRONOME_MARK"
    persistent: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "before"

    def __post_init__(self):
        if self.reference_duration:
            assert isinstance(self.reference_duration, _duration.Duration), repr(
                self.reference_duration
            )
        if isinstance(self.units_per_minute, float):
            raise Exception(
                f"do not set units-per-minute to float ({self.units_per_minute});"
                " use fraction with decimal override instead."
            )
        prototype = (int, fractions.Fraction, collections.abc.Sequence, type(None))
        assert isinstance(self.units_per_minute, prototype)
        if isinstance(self.units_per_minute, collections.abc.Sequence):
            assert len(self.units_per_minute) == 2
            item_prototype = (int, _duration.Duration)
            assert all(isinstance(_, item_prototype) for _ in self.units_per_minute)
        assert isinstance(self.textual_indication, str | type(None))
        if self.custom_markup is not None:
            assert isinstance(self.custom_markup, Markup)
        if self.decimal is not None:
            assert isinstance(self.decimal, bool | str), repr(self.decimal)
        assert isinstance(self.hide, bool), repr(self.hide)

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a metronome mark with quarters per minute greater
        than that of this metronome mark.
        """
        assert isinstance(argument, type(self)), repr(argument)
        self_quarters_per_minute = self.quarters_per_minute or 0
        argument_quarters_per_minute = argument.quarters_per_minute or 0
        assert isinstance(self_quarters_per_minute, int | float | fractions.Fraction)
        assert isinstance(
            argument_quarters_per_minute, (int, float, fractions.Fraction)
        )
        return self_quarters_per_minute < argument_quarters_per_minute

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
        elif isinstance(self.units_per_minute, fractions.Fraction):
            markup = MetronomeMark.make_tempo_equation_markup(
                self.reference_duration,
                self.units_per_minute,
                decimal=self.decimal,
            )
            string = markup.string
            return string
        string = f"{self._dotted}={self.units_per_minute}"
        return string

    def _get_lilypond_format(self):
        equation = None
        if self.reference_duration is not None and self.units_per_minute is not None:
            equation = self._equation
        if self.custom_markup is not None:
            return rf"\tempo {self.custom_markup.string}"
        elif self.textual_indication and equation:
            return rf"\tempo {self.textual_indication} {equation}"
        elif equation:
            return rf"\tempo {equation}"
        elif self.textual_indication:
            return rf"\tempo {self.textual_indication}"
        else:
            return r"\tempo \default"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        if not self.hide:
            contributions.before.commands.append(self._get_lilypond_format())
        return contributions

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
        markup = Markup(rf"\markup {string}")
        return markup

    def _get_markup_arguments(self):
        assert self.custom_markup is None
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        dot_count = self.reference_duration.dot_count
        stem_height = 1
        if not self.decimal:
            return {
                "duration_log": duration_log,
                "dot_count": dot_count,
                "stem_height": stem_height,
                "base": self.units_per_minute,
            }
        if isinstance(self.decimal, str):
            return (duration_log, dot_count, stem_height, self.decimal)
        assert self.decimal is True, repr(self.decimal)
        fraction = fractions.Fraction(self.units_per_minute)
        n, d = fraction.numerator, fraction.denominator
        base = n // d
        n = n % d
        return {
            "duration_log": duration_log,
            "dot_count": dot_count,
            "stem_height": stem_height,
            "base": base,
            "n": n,
            "d": d,
        }

    @property
    def is_imprecise(self) -> bool:
        """
        Is true if metronome mark is entirely textual or if metronome mark's
        units_per_minute is a range.

        ..  container:: example

            Imprecise metronome marks:

            >>> duration = abjad.Duration(1, 4)

            >>> abjad.MetronomeMark(textual_indication="Langsam").is_imprecise
            True

            >>> abjad.MetronomeMark(duration, (35, 50), "Langsam").is_imprecise
            True

            >>> abjad.MetronomeMark(duration, (35, 50)).is_imprecise
            True

            Precise metronome marks:

            >>> abjad.MetronomeMark(duration, 60).is_imprecise
            False

            >>> abjad.MetronomeMark(duration, 60, "Langsam").is_imprecise
            False

        """
        if self.reference_duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def quarters_per_minute(self) -> tuple | None | fractions.Fraction:
        """
        Gets metronome mark quarters per minute.

        ..  container:: example

            >>> mark = abjad.MetronomeMark(abjad.Duration(1, 8), 52)
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
        return fractions.Fraction(result)

    def duration_to_milliseconds(self, duration) -> _duration.Duration:
        """
        Gets millisecond value of ``duration`` under a given metronome mark.

        Dotted sixteenth lasts 1500 msec at quarter equals 60:

        ..  container:: example

            >>> mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> mark.duration_to_milliseconds((3, 8))
            Duration(1500, 1)

        """
        assert isinstance(self.reference_duration, _duration.Duration)
        denominator = self.reference_duration.denominator
        numerator = self.reference_duration.numerator
        whole_note_duration = fractions.Fraction(1000)
        whole_note_duration *= fractions.Fraction(denominator, numerator)
        whole_note_duration *= fractions.Fraction(60, self.units_per_minute)
        duration = _duration.Duration(duration)
        return _duration.Duration(duration * whole_note_duration)

    @staticmethod
    def make_tempo_equation_markup(
        reference_duration, units_per_minute, *, decimal=False
    ) -> Markup:
        r"""
        Makes tempo equation markup.

        Integer-valued metronome mark:

        ..  container:: example

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

            >>> import fractions
            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     abjad.Duration(1, 4),
            ...     fractions.Fraction(272, 3),
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
            units_per_minute, fractions.Fraction
        ) and not _math.is_integer_equivalent_number(units_per_minute):
            if decimal:
                decimal_: float | str
                if decimal is True:
                    decimal_ = float(units_per_minute)
                else:
                    assert isinstance(decimal, str), repr(decimal)
                    decimal_ = decimal
                markup = Markup(
                    r"\markup \abjad-metronome-mark-markup"
                    f' #{log} #{dots} #{stem} #"{decimal_}"'
                )
            else:
                nonreduced = fractions.Fraction(units_per_minute)
                base = int(nonreduced)
                remainder = nonreduced - base
                n, d = remainder.numerator, remainder.denominator
                markup = Markup(
                    r"\markup \abjad-metronome-mark-mixed-number-markup"
                    f" #{log} #{dots} #{stem}"
                    f' #"{base}" #"{n}" #"{d}"'
                )
        else:
            markup = Markup(
                r"\markup \abjad-metronome-mark-markup"
                f' #{log} #{dots} #{stem} #"{units_per_minute}"'
            )
        return markup


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Ottava:
    r"""
    LilyPond ``\ottava`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> ottava = abjad.Ottava(n=1)
        >>> abjad.attach(ottava, staff[0])
        >>> ottava = abjad.Ottava(n=0, site="after")
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

    n: int = 0
    _: dataclasses.KW_ONLY
    # TODO: maybe implement "leak" instead of "site"?
    site: str = "before"

    context: typing.ClassVar[str] = "Staff"
    # find_context_on_attach: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.n, int), repr(self.n)
        assert isinstance(self.site, str), repr(self.site)

    def _before_attach(self, deactivate, component):
        for indicator in component._get_indicators():
            if isinstance(indicator, type(self)) and indicator.site == self.site:
                classname = type(component).__name__
                message = f"can not attach {self!r} to {classname}:"
                message += f"\n    {indicator!r} is already attached to {classname}."
                raise Exception(message)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        n = self.n or 0
        string = rf"\ottava {n}"
        if self.site in ("before", None):
            contributions.before.commands.append(string)
        else:
            assert self.site == "after"
            contributions.after.commands.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> staff = abjad.Staff([note])
        >>> score = abjad.Score([staff], name="Score")
        >>> mark = abjad.RehearsalMark(markup="A")
        >>> bundle = abjad.bundle(mark, r"\tweak color #blue")
        >>> abjad.attach(bundle, note)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \new Staff
                {
                    \tweak color #blue
                    \mark A
                    c'4
                }
            >>

    """

    markup: Markup | str | None = None
    number: int | None = None

    # find_context_on_attach: typing.ClassVar[bool] = True
    context: typing.ClassVar[str] = "Score"

    def __post_init__(self):
        if self.markup is not None:
            assert isinstance(self.markup, str | Markup), repr(self.markup)
        if self.number is not None:
            assert isinstance(self.number, int), repr(self.number)

    def _get_lilypond_format(self):
        if self.markup is not None:
            result = rf"\mark {self.markup}"
        elif self.number is not None:
            result = rf"\mark #{self.number}"
        else:
            result = r"\mark \default"
        return result

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format()
        contributions.opening.commands.append(string)
        return contributions

    @staticmethod
    def from_string(string) -> "RehearsalMark":
        """
        Makes rehearsal mark from ``string``.

        ..  container:: example

            >>> abjad.RehearsalMark.from_string("A")
            RehearsalMark(markup=None, number=1)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string("AA")
            RehearsalMark(markup=None, number=27)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string("AB")
            RehearsalMark(markup=None, number=28)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string("BA")
            RehearsalMark(markup=None, number=53)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string("BB")
            RehearsalMark(markup=None, number=54)

        """
        number = 0
        for place, letter in enumerate(reversed(string)):
            integer = ord(letter) - ord("A") + 1
            multiplier = 26**place
            integer *= multiplier
            number += integer
        return RehearsalMark(number=number)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Repeat:
    r"""
    Repeat.

    ..  container:: example

        Volta repeat:

        >>> container = abjad.Container("c'4 d'4 e'4 f'4")
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff])
        >>> repeat = abjad.Repeat()
        >>> abjad.attach(repeat, container)
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
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff])
        >>> repeat = abjad.Repeat(repeat_type='unfold')
        >>> abjad.attach(repeat, container)
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

    can_attach_to_containers: typing.ClassVar[bool] = True
    format_leaf_children: typing.ClassVar[bool] = False
    # find_context_on_attach: typing.ClassVar[bool] = True
    context: typing.ClassVar[str] = "Score"
    site: typing.ClassVar[str] = "before"

    def __post_init__(self):
        assert isinstance(self.repeat_count, int), repr(self.repeat_count)
        assert isinstance(self.repeat_type, str), repr(self.repeat_type)

    def _get_lilypond_format(self):
        return rf"\repeat {self.repeat_type} {self.repeat_count}"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        contributions.before.commands.append(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RepeatTie:
    r"""
    LilyPond ``\repeatTie`` command.

    ..  container:: example

        >>> voice = abjad.Voice("c'4 c' d' d'", name="Voice")
        >>> repeat_tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(repeat_tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                c'4
                c'4
                - \tweak color #blue
                \repeatTie
                d'4
                d'4
            }

        >>> abjad.get.indicators(voice[1], abjad.RepeatTie)
        [RepeatTie()]

        >>> wrapper = abjad.get.indicator(voice[1], abjad.RepeatTie, unwrap=False)
        >>> wrapper.get_item()
        Bundle(indicator=RepeatTie(), tweaks=(Tweak(string='- \\tweak color #blue', tag=None),))

        >>> for leaf in voice:
        ...     leaf, abjad.get.logical_tie(leaf)
        ...
        (Note("c'4"), LogicalTie(items=[Note("c'4"), Note("c'4")]))
        (Note("c'4"), LogicalTie(items=[Note("c'4"), Note("c'4")]))
        (Note("d'4"), LogicalTie(items=[Note("d'4")]))
        (Note("d'4"), LogicalTie(items=[Note("d'4")]))

    ..  container:: example

        With ``direction`` unset:

        >>> voice = abjad.Voice("c'4 c'4 c''4 c''4", name="Voice")
        >>> tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[1])
        >>> tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[3])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
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

        With ``direction=abjad.UP``:

        >>> voice = abjad.Voice("c'4 c'4 c''4 c''4", name="Voice")
        >>> tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[1], direction=abjad.UP)
        >>> tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[3], direction=abjad.UP)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
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

        With ``direction=abjad.DOWN``:

        >>> voice = abjad.Voice("c'4 c'4 c''4 c''4", name="Voice")
        >>> tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[1], direction=abjad.DOWN)
        >>> tie = abjad.RepeatTie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, voice[3], direction=abjad.DOWN)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
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

    """

    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    # find_context_on_attach: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True

    def _attachment_test_all(self, argument):
        if not (
            hasattr(argument, "written_pitch") or hasattr(argument, "written_pitches")
        ):
            string = f"Must be note or chord (not {argument})."
            return [string]
        return True

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        strings = []
        if wrapper.direction is not None:
            string = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
            strings.append(string)
        strings.append(r"\repeatTie")
        contributions.after.spanner_starts.extend(strings)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ShortInstrumentName:
    r"""
    LilyPond ``\shortInstrumentName`` command.

    ..  container:: example

        Set ``\shortInstrumentName`` to markup like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> short_instrument_name = abjad.ShortInstrumentName(r"\markup Vc.")
        >>> abjad.attach(short_instrument_name, staff[0])
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

        Set ``\shortInstrumentName`` to custom function like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> short_instrument_name = abjad.ShortInstrumentName(r"\my_custom_function")
        >>> abjad.attach(short_instrument_name, staff[0])

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set Staff.shortInstrumentName = \my_custom_function
                c'4
                d'4
                e'4
                f'4
            }

    """

    markup: typing.Union[str, Markup]
    _: dataclasses.KW_ONLY
    context: str = "Staff"
    site: str = "before"

    latent: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    redraw: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.markup, str | Markup), repr(self.markup)
        assert isinstance(self.context, str), repr(self.context)
        assert isinstance(self.site, str), repr(self.site)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        site = getattr(contributions, self.site)
        site.commands.extend(self._get_lilypond_format())
        return contributions

    def _get_lilypond_format(self, context=None):
        result = []
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._get_lilypond_type()
        if isinstance(self.markup, Markup):
            string = self.markup.string
        else:
            assert isinstance(self.markup, str)
            string = self.markup
        string = rf"\set {context!s}.shortInstrumentName = {string}"
        result.append(string)
        return result

    def _get_lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StaffChange:
    r"""
    Staff change.

    ..  container:: example

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

    """

    staff_name: str | bool

    context: typing.ClassVar[str] = "Staff"
    format_leaf_children: typing.ClassVar[bool] = False
    site: typing.ClassVar[str] = "before"
    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT

    def __post_init__(self):
        assert isinstance(self.staff_name, str | bool), repr(self.staff_name)
        if isinstance(self.staff_name, bool):
            assert self.staff_name is False, repr(self.staff_name)

    def _get_lilypond_format(self):
        if self.staff_name is False:
            return r"\change Staff = ##f"
        return rf"\change Staff = {self.staff_name}"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        contributions.opening.commands.append(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StartBeam:
    r"""
    LilyPond ``[`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> start_beam = abjad.StartBeam()
        >>> bundle = abjad.bundle(start_beam, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

        With ``direction=abjad.DOWN``:

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> start_beam = abjad.StartBeam()
        >>> bundle = abjad.bundle(start_beam, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0], direction=abjad.DOWN)
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
                _ [
                d'8
                e'8
                f'8
                ]
            }

    """

    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "BEAM"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    def _add_direction(self, string, wrapper):
        if wrapper.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
            string = f"{symbol} {string}"
        return string

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._add_direction("[", wrapper)
        contributions.after.start_beam.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StartGroup:
    r"""
    LilyPond ``\startGroup`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_group = abjad.StartGroup()
        >>> bundle = abjad.bundle(start_group, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

    """

    context: typing.ClassVar[str] = "Voice"
    nestable_spanner: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = r"\startGroup"
        contributions.after.spanner_starts.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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

        Diminuendo:

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

        Diminuendo al niente:

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

        Subito diminuendo:

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

        Subito diminuendo al niente:

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
        >>> bundle = abjad.bundle(start_hairpin, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

    context: typing.ClassVar[str] = "Voice"
    crescendo_start: typing.ClassVar[str] = r"\<"
    decrescendo_start: typing.ClassVar[str] = r"\>"
    directed: typing.ClassVar[bool] = True
    known_shapes = ("<", "o<", "<|", "o<|", ">", ">o", "|>", "|>o", "--")
    parameter: typing.ClassVar[str] = "DYNAMIC"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "after"
    spanner_start: typing.ClassVar[bool] = True
    trend: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert self.shape in self.known_shapes, repr(self.shape)

    def _add_direction(self, string, *, wrapper=None):
        if wrapper.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
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

    def _get_lilypond_format(self, *, wrapper=None):
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
            string = self.crescendo_start
            string = self._add_direction(string, wrapper=wrapper)
            strings.append(string)
        elif ">" in self.shape:
            string = self.decrescendo_start
            string = self._add_direction(string, wrapper=wrapper)
            strings.append(string)
        else:
            raise ValueError(self.shape)
        return strings

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        strings = self._get_lilypond_format(wrapper=wrapper)
        contributions.after.spanner_starts.extend(strings)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StartPhrasingSlur:
    r"""
    LilyPond ``(`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> bundle = abjad.bundle(start_phrasing_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

    """

    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "PHRASING_SLUR"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    def _add_direction(self, string, *, wrapper=None):
        if wrapper.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
            string = f"{symbol} {string}"
        return string

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._add_direction(r"\(", wrapper=wrapper)
        contributions.after.spanner_starts.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StartPianoPedal:
    r"""
    LilyPond ``\sustainOn``, ``\sostenutoOn``, ``\unaCorda`` commands.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> bundle = abjad.bundle(
        ...     start_piano_pedal,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak parent-alignment-X #center",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[1])

        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> bundle = abjad.bundle(start_piano_pedal, r"- \tweak color #red")
        >>> abjad.attach(bundle, staff[1])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[2])

        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> bundle = abjad.bundle(start_piano_pedal, r"- \tweak color #green")
        >>> abjad.attach(bundle, staff[2])
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

    """

    # TODO: change "kind" to "command" with "\unaCorda", "\sostenutoOn", "\sustainOn"
    kind: str = "sustain"

    context: typing.ClassVar[str] = "StaffGroup"
    parameter: typing.ClassVar[str] = "PEDAL"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert self.kind in ("sustain", "sostenuto", "corda"), repr(self.kind)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        if self.kind == "corda":
            string = r"\unaCorda"
        elif self.kind == "sostenuto":
            string = r"\sostenutoOn"
        else:
            assert self.kind == "sustain"
            string = r"\sustainOn"
        contributions.after.spanner_starts.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StartSlur:
    r"""
    LilyPond ``(`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_slur = abjad.StartSlur()
        >>> bundle = abjad.bundle(start_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

        With ``direction=abjad.UP``:

        >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
        >>> abjad.attach(abjad.StartSlur(), staff[0], direction=abjad.UP)
        >>> abjad.attach(abjad.StopSlur(), staff[3])
        >>> abjad.attach(abjad.StartSlur(), staff[4], direction=abjad.UP)
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

        With ``direction=abjad.DOWN``:

        >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
        >>> abjad.attach(abjad.StartSlur(), staff[0], direction=abjad.DOWN)
        >>> abjad.attach(abjad.StopSlur(), staff[3])
        >>> abjad.attach(abjad.StartSlur(), staff[4], direction=abjad.DOWN)
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

    """

    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "SLUR"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    def _add_direction(self, string, *, wrapper=None):
        if wrapper.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
            string = f"{symbol} {string}"
        return string

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._add_direction("(", wrapper=wrapper)
        contributions.after.spanner_starts.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> abjad.StartTextSpan()
        StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, concat_hspace_right=None, left_broken_text=None, left_text=None, right_padding=None, right_text=None, style=None)

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")

        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> bundle = abjad.bundle(
        ...     start_text_span,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak staff-padding 2.5",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])

        >>> start_text_span = abjad.StartTextSpan(
        ...     command=r"\startTextSpanOne",
        ...     left_text=abjad.Markup(r"\upright A"),
        ...     right_text=abjad.Markup(r"\markup \upright B"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> bundle = abjad.bundle(
        ...     start_text_span,
        ...     r"- \tweak color #red",
        ...     r"- \tweak staff-padding 6",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> stop_text_span = abjad.StopTextSpan(command=r"\stopTextSpanOne")
        >>> abjad.attach(stop_text_span, staff[-1])

        >>> markup = abjad.Markup(r"\markup SPACER")
        >>> bundle = abjad.bundle(markup, r"- \tweak transparent ##t")
        >>> abjad.attach(bundle, staff[0], direction=abjad.UP)
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
                - \tweak color #blue
                - \tweak staff-padding 2.5
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                \startTextSpan
                - \tweak color #red
                - \tweak staff-padding 6
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright A \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright B
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-dashed-line-with-hook
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-invisible-line
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
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
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
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
                - \tweak staff-padding 2.5
                - \abjad-solid-line-with-hook
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

        Styles constrained to ``'dashed-line-with-arrow'``, ``'dashed-line-with-hook'``,
        ``'invisible-line'``, ``'solid-line-with-arrow'``, ``'solid-line-with-hook'``,
        none.

    """

    command: str = r"\startTextSpan"
    concat_hspace_left: int | float = 0.5
    concat_hspace_right: int | float | None = None
    left_broken_text: bool | str | Markup | None = None
    left_text: str | Markup | None = None
    right_padding: int | float | None = None
    right_text: str | Markup | None = None
    style: str | None = None

    allow_multiple_with_different_values: typing.ClassVar[bool] = True
    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "TEXT_SPANNER"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    _styles = (
        "dashed-line-with-arrow",
        "dashed-line-with-hook",
        "dashed-line-with-up-hook",
        "invisible-line",
        "solid-line-with-arrow",
        "solid-line-with-hook",
        "solid-line-with-up-hook",
    )

    def __post_init__(self):
        assert isinstance(self.command, str), repr(self.command)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        if self.style is not None:
            string = rf"- \abjad-{self.style}"
            contributions.after.spanner_starts.append(string)
        if self.left_text:
            string = self._get_left_text_directive()
            contributions.after.spanner_starts.append(string)
        if self.left_broken_text is not None:
            string = self._get_left_broken_text_tweak()
            contributions.after.spanner_starts.append(string)
        if self.right_text:
            string = self._get_right_text_tweak()
            contributions.after.spanner_starts.append(string)
        if self.right_padding:
            string = self._get_right_padding_tweak()
            contributions.after.spanner_starts.append(string)
        string = self._add_direction(self.command, wrapper=wrapper)
        contributions.after.spanner_starts.append(string)
        return contributions

    def _add_direction(self, string, *, wrapper=None):
        if wrapper.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
            string = f"{symbol} {string}"
        return string

    def _get_left_broken_text_tweak(self):
        if isinstance(self.left_broken_text, str):
            left_broken_text = self.left_broken_text
        else:
            left_broken_text = self.left_broken_text.string
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "left-broken", "text"),
            value=left_broken_text,
        )
        string = override.tweak_string(self)
        return string

    def _get_left_text_directive(self):
        if isinstance(self.left_text, str):
            return self.left_text
        left_text_string = self.left_text.string
        left_text_string = left_text_string.removeprefix(r"\markup").strip()
        hspace_string = rf"\hspace #{self.concat_hspace_left}"
        markup = Markup(rf"\markup \concat {{ {left_text_string} {hspace_string} }}")
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "left", "text"),
            value=markup.string,
        )
        string = override.tweak_string()
        return string

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
            return self.right_text
        if self.concat_hspace_right is not None:
            number = self.concat_hspace_right
            right_text = self.right_text.string
            markup = Markup(rf"\markup \concat {{ {right_text} \hspace #{number} }}")
        else:
            markup = self.right_text
        if isinstance(markup, str):
            value = markup
        else:
            assert isinstance(markup, Markup)
            value = markup.string
        override = _overrides.LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "right", "text"),
            value=value,
        )
        string = override.tweak_string()
        return string

    def _get_start_command(self):
        string = self._get_parameter_name()
        return rf"\start{string}"


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StartTrillSpan:
    r"""
    LilyPond ``\startTrillSpan`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_trill_span = abjad.StartTrillSpan()
        >>> bundle = abjad.bundle(start_trill_span, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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
        >>> start_trill_span = abjad.StartTrillSpan(interval=abjad.NamedInterval("M2"))
        >>> bundle = abjad.bundle(start_trill_span, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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
        >>> start_trill_span = abjad.StartTrillSpan(pitch=abjad.NamedPitch("C#4"))
        >>> bundle = abjad.bundle(start_trill_span, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

    """

    interval: str | _pitch.NamedInterval | None = None
    pitch: str | _pitch.NamedPitch | None = None

    context: typing.ClassVar[str] = "Voice"
    parameter: typing.ClassVar[str] = "TRILL"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_start: typing.ClassVar[bool] = True

    def __post_init__(self):
        if self.interval is not None:
            assert isinstance(self.interval, _pitch.NamedInterval), repr(self.interval)
        if self.pitch is not None:
            assert isinstance(self.pitch, _pitch.NamedPitch), repr(self.pitch)

    def _get_contributions(self, *, component=None):
        contributions = _contributions.ContributionsBySite()
        string = r"\startTrillSpan"
        if self.interval or self.pitch:
            contributions.opening.pitched_trill.append(r"\pitchedTrill")
            if self.pitch:
                pitch = self.pitch
            else:
                pitch = component.written_pitch + self.interval
            string = string + f" {pitch.name}"
        # NOTE: crucial to use after.trill_spanner_starts here:
        contributions.after.trill_spanner_starts.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
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

    site: typing.ClassVar[str] = "after"
    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.MIDDLE

    def __post_init__(self):
        if not _math.is_nonnegative_integer_power_of_two(self.tremolo_flags):
            raise ValueError(f"nonnegative integer power of 2: {self.tremolo_flags!r}.")

    def _get_lilypond_format(self):
        return f":{self.tremolo_flags!s}"

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        contributions.after.stem_tremolos.append(self._get_lilypond_format())
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopBeam:
    r"""
    LilyPond ``]`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'8 d' e' r")
        >>> start_beam = abjad.StartBeam()
        >>> bundle = abjad.bundle(start_beam, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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
        >>> start_beam = abjad.StartBeam()
        >>> bundle = abjad.bundle(start_beam, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_beam = abjad.StopBeam(leak=True)
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
                <>
                ]
                r8
            }

    """

    leak: bool = dataclasses.field(default=False, compare=False)

    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT
    context: typing.ClassVar[str] = "Voice"
    parameter: typing.ClassVar[str] = "BEAM"
    persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = "]"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.stop_beam.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopGroup:
    r"""
    LilyPond ``\stopGroup`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_group = abjad.StartGroup()
        >>> bundle = abjad.bundle(start_group, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_group = abjad.StopGroup()
        >>> abjad.attach(stop_group, staff[-2])
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
        >>> start_group = abjad.StartGroup()
        >>> bundle = abjad.bundle(start_group, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_group = abjad.StopGroup(leak=True)
        >>> abjad.attach(stop_group, staff[-2])
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
                <>
                \stopGroup
                r4
            }

    ..  container:: example

        REGRESSION. Leaked contributions appear last in postevent format site:

        >>> staff = abjad.Staff("c'8 d' e' f' r2")
        >>> abjad.beam(staff[:4])
        >>> start_group = abjad.StartGroup()
        >>> bundle = abjad.bundle(start_group, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_group = abjad.StopGroup(leak=True)
        >>> abjad.attach(stop_group, staff[3])
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
                <>
                \stopGroup
                r2
            }

        The leaked text spanner above does not inadvertantly leak the beam.

    """

    leak: bool = dataclasses.field(default=False, compare=False)

    context: typing.ClassVar[str] = "Voice"
    nestable_spanner: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True
    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = r"\stopGroup"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.spanner_stops.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopHairpin:
    r"""
    LilyPond ``\!`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_hairpin = abjad.StartHairpin('<')
        >>> bundle = abjad.bundle(start_hairpin, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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
        >>> bundle = abjad.bundle(start_hairpin, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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
                <>
                \!
                r4
            }

    """

    leak: bool = dataclasses.field(default=False, compare=False)

    context: typing.ClassVar[str] = "Voice"
    # TODO: should these be uncommented?
    # parameter: typing.ClassVar[str] = "DYNAMIC"
    # persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = r"\!"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.spanner_stops.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopPhrasingSlur:
    r"""
    LilyPond ``\)`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> bundle = abjad.bundle(start_phrasing_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_phrasing_slur = abjad.StopPhrasingSlur()
        >>> abjad.attach(stop_phrasing_slur, staff[-2])
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
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> bundle = abjad.bundle(start_phrasing_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_phrasing_slur = abjad.StopPhrasingSlur(leak=True)
        >>> abjad.attach(stop_phrasing_slur, staff[-2])
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
                <>
                \)
                r4
            }

    ..  container:: example

        REGRESSION. Leaked contributions appear last in postevent format site:

        >>> staff = abjad.Staff("c'8 d' e' f' r2")
        >>> abjad.beam(staff[:4])
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> bundle = abjad.bundle(start_phrasing_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_phrasing_slur = abjad.StopPhrasingSlur(leak=True)
        >>> abjad.attach(stop_phrasing_slur, staff[3])
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
                <>
                \)
                r2
            }

        The leaked text spanner above does not inadvertantly leak the beam.

    """

    leak: bool = dataclasses.field(default=False, compare=False)

    context: typing.ClassVar[str] = "Voice"
    parameter: typing.ClassVar[str] = "PHRASING_SLUR"
    persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = r"\)"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.spanner_stops.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopPianoPedal:
    r"""
    LilyPond ``\sostenutoOff``, ``\sustainOff``, ``\treCorde`` commands.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> bundle = abjad.bundle(
        ...     start_piano_pedal,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak parent-alignment-X #center",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> bundle = abjad.bundle(
        ...     stop_piano_pedal,
        ...     r"- \tweak color #red",
        ...     r"- \tweak parent-alignment-X #center",
        ... )
        >>> abjad.attach(bundle, staff[-2])
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
        >>> bundle = abjad.bundle(
        ...     start_piano_pedal,
        ...     r"- \tweak color #blue",
        ...     r"- \tweak parent-alignment-X #center",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal(leak=True)
        >>> bundle = abjad.bundle(
        ...     stop_piano_pedal,
        ...     r"- \tweak color #red",
        ...     r"- \tweak parent-alignment-X #center",
        ... )
        >>> abjad.attach(bundle, staff[-2])
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

    """

    # TODO: change "kind" to "command"
    kind: str = "sustain"
    leak: bool = dataclasses.field(default=False, compare=False)

    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT
    context: typing.ClassVar[str] = "StaffGroup"
    parameter: typing.ClassVar[str] = "PEDAL"
    persistent: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert self.kind in ("sustain", "sostenuto", "corda")
        assert isinstance(self.leak, bool), repr(self.leak)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        if self.kind == "corda":
            command = r"\treCorde"
        elif self.kind == "sostenuto":
            command = r"\sostenutoOff"
        else:
            assert self.kind == "sustain"
            command = r"\sustainOff"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(command)
        else:
            contributions.after.spanner_stops.append(command)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopSlur:
    r"""
    LilyPond ``)`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_slur = abjad.StartSlur()
        >>> bundle = abjad.bundle(start_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_slur = abjad.StopSlur()
        >>> abjad.attach(stop_slur, staff[-2])
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
        >>> start_slur = abjad.StartSlur()
        >>> bundle = abjad.bundle(start_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_slur = abjad.StopSlur(leak=True)
        >>> abjad.attach(stop_slur, staff[-2])
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
                <>
                )
                r4
            }

    ..  container:: example

        REGRESSION. Leaked contributions appear last in postevent format site.
        The leaked text spanner above does not inadvertantly leak the beam:

        >>> staff = abjad.Staff("c'8 d' e' f' r2")
        >>> abjad.beam(staff[:4])
        >>> start_slur = abjad.StartSlur()
        >>> bundle = abjad.bundle(start_slur, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_slur = abjad.StopSlur(leak=True)
        >>> abjad.attach(stop_slur, staff[3])
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
                <>
                )
                r2
            }


    """

    leak: bool = dataclasses.field(default=False, compare=False)

    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT
    context: typing.ClassVar[str] = "Voice"
    parameter: typing.ClassVar[str] = "SLUR"
    persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.leak, bool), repr(self.leak)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = ")"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.spanner_stops.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopTextSpan:
    r"""
    LilyPond ``\stopTextSpan`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-2])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak staff-padding 2.5
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                r4
            }

        With leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\markup \upright tasto"),
        ...     style="dashed-line-with-arrow",
        ... )
        >>> bundle = abjad.bundle(start_text_span, r"- \tweak staff-padding 2.5")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_text_span = abjad.StopTextSpan(leak=True)
        >>> abjad.attach(stop_text_span, staff[-2])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak staff-padding 2.5
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup \upright tasto
                \startTextSpan
                d'4
                e'4
                <>
                \stopTextSpan
                r4
            }

    """

    command: str = r"\stopTextSpan"
    leak: bool = dataclasses.field(default=False, compare=False)

    context: typing.ClassVar[str] = "Voice"
    enchained: typing.ClassVar[bool] = True
    nestable_spanner: typing.ClassVar[bool] = True
    parameter: typing.ClassVar[str] = "TEXT_SPANNER"
    persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.command, str), repr(self.command)
        assert self.command.startswith("\\"), repr(self.command)
        assert isinstance(self.leak, bool), repr(self.leak)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = self.command
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.spanner_stops.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StopTrillSpan:
    r"""
    LilyPond ``\stopTrillSpan`` command.

    ..  container:: example

        Without leak:

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_trill_span = abjad.StartTrillSpan()
        >>> bundle = abjad.bundle(start_trill_span, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_trill_span = abjad.StopTrillSpan()
        >>> abjad.attach(stop_trill_span, staff[-2])
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
        >>> start_trill_span = abjad.StartTrillSpan()
        >>> bundle = abjad.bundle(start_trill_span, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
        >>> stop_trill_span = abjad.StopTrillSpan(leak=True)
        >>> abjad.attach(stop_trill_span, staff[-2])
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
                <>
                \stopTrillSpan
                r4
            }

    """

    leak: bool = dataclasses.field(default=False, compare=False)

    time_orientation: typing.ClassVar[_enums.Horizontal] = _enums.RIGHT
    context: typing.ClassVar[str] = "Voice"
    parameter: typing.ClassVar[str] = "TRILL"
    persistent: typing.ClassVar[bool] = True
    spanner_stop: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.leak, bool), repr(self.leak)

    def _get_contributions(self, component=None):
        contributions = _contributions.ContributionsBySite()
        string = r"\stopTrillSpan"
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.after.spanner_stops.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tie:
    r"""
    LilyPond ``~`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> tie = abjad.Tie()
        >>> bundle = abjad.bundle(tie, r"- \tweak color #blue")
        >>> abjad.attach(bundle, staff[0])
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

        With ``direction=abjad.UP``:

        >>> staff = abjad.Staff("c'4 c' c'' c''")
        >>> abjad.attach(abjad.Tie(), staff[0], direction=abjad.UP)
        >>> abjad.attach(abjad.Tie(), staff[2], direction=abjad.UP)
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

        With ``direction=abjad.DOWN``:

        >>> staff = abjad.Staff("c'4 c' c'' c''")
        >>> abjad.attach(abjad.Tie(), staff[0], direction=abjad.DOWN)
        >>> abjad.attach(abjad.Tie(), staff[2], direction=abjad.DOWN)
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

    """

    context: typing.ClassVar[str] = "Voice"
    directed: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True

    def _add_direction(self, string, *, wrapper=None):
        if wrapper.direction is not None:
            symbol = _string.to_tridirectional_lilypond_symbol(wrapper.direction)
            string = f"{symbol} {string}"
        return string

    def _attachment_test_all(self, argument):
        if not (
            hasattr(argument, "written_pitch") or hasattr(argument, "written_pitches")
        ):
            string = f"Must be note or chord (not {argument})."
            return [string]
        return True

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._add_direction("~", wrapper=wrapper)
        strings = [string]
        contributions.after.spanner_starts.extend(strings)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class TimeSignature:
    r"""
    Time signature.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8")
        >>> score = abjad.Score([staff], name="Score")
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
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0], context="Score")
        >>> score[:] = []

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
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(
        ...     time_signature,
        ...     staff[0],
        ...     context="Score",
        ...     tag=abjad.Tag("+PARTS"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(score, tags=True)
        >>> print(string)
        \context Score = "Score"
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
        >>> score = abjad.Score([staff], name="Score")
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
    hide: bool = dataclasses.field(compare=False, default=False)
    partial: _duration.Duration | None = None

    check_effective_context: typing.ClassVar[bool] = True
    context: typing.ClassVar[str] = "Score"
    persistent: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "before"

    def __post_init__(self):
        assert isinstance(self.pair, tuple), repr(self.pair)
        assert len(self.pair) == 2, repr(self.pair)
        assert isinstance(self.pair[0], int)
        assert isinstance(self.pair[1], int)
        if self.partial is not None:
            assert isinstance(self.partial, _duration.Duration), repr(self.partial)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        if self.is_non_dyadic_rational and not self.hide:
            string = '#(ly:expect-warning "strange time signature found")'
            contributions.before.commands.append(string)
        strings = self._get_lilypond_format()
        contributions.opening.commands.extend(strings)
        return contributions

    def _get_lilypond_format(self):
        result = []
        if self.hide:
            return result
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
            >>> score = abjad.Score([staff], name="Score")
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
    def implied_prolation(self) -> fractions.Fraction:
        """
        Gets implied prolation of time signature.

        ..  container:: example

            Implied prolation of dyadic time signature:

            >>> abjad.TimeSignature((3, 8)).implied_prolation
            Fraction(1, 1)

            Implied prolation of nondyadic time signature:

            >>> abjad.TimeSignature((7, 12)).implied_prolation
            Fraction(2, 3)

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

    def to_dyadic_rational(self) -> "TimeSignature":
        """
        Makes new time signature equivalent to current time signature with power-of-two
        denominator.

        ..  container:: example

            >>> abjad.TimeSignature((1, 12)).to_dyadic_rational()
            TimeSignature(pair=(1, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((2, 12)).to_dyadic_rational()
            TimeSignature(pair=(2, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((3, 12)).to_dyadic_rational()
            TimeSignature(pair=(2, 8), hide=False, partial=None)

            >>> abjad.TimeSignature((4, 12)).to_dyadic_rational()
            TimeSignature(pair=(4, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((5, 12)).to_dyadic_rational()
            TimeSignature(pair=(5, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((6, 12)).to_dyadic_rational()
            TimeSignature(pair=(4, 8), hide=False, partial=None)

            >>> abjad.TimeSignature((1, 14)).to_dyadic_rational()
            TimeSignature(pair=(1, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((2, 14)).to_dyadic_rational()
            TimeSignature(pair=(2, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((3, 14)).to_dyadic_rational()
            TimeSignature(pair=(3, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((4, 14)).to_dyadic_rational()
            TimeSignature(pair=(4, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((5, 14)).to_dyadic_rational()
            TimeSignature(pair=(5, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((6, 14)).to_dyadic_rational()
            TimeSignature(pair=(6, 14), hide=False, partial=None)

        """
        non_power_of_two_denominator = self.denominator
        power_of_two_denominator = _math.greatest_power_of_two_less_equal(
            non_power_of_two_denominator
        )
        pair = _duration.with_denominator(self.pair, power_of_two_denominator)
        return type(self)(pair)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class VoiceNumber:
    r"""
    LilyPond ``\voiceOne``, ``\voiceTwo``, ``\voiceThree``, ``\voiceFour``,
    ``\oneVoice`` commands.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> voice_1 = abjad.Voice("g'8 a' b' c''")
        >>> command = abjad.VoiceNumber(n=1)
        >>> abjad.attach(command, voice_1[0])
        >>> voice_2 = abjad.Voice("e'8 f' g' a'")
        >>> command = abjad.VoiceNumber(n=2)
        >>> abjad.attach(command, voice_2[0])
        >>> container = abjad.Container([voice_1, voice_2], simultaneous=True)
        >>> staff.append(container)
        >>> voice = abjad.Voice("c''4 a'")
        >>> command = abjad.VoiceNumber()
        >>> abjad.attach(command, voice[0])
        >>> staff.append(voice)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <<
                    \new Voice
                    {
                        \voiceOne
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                    \new Voice
                    {
                        \voiceTwo
                        e'8
                        f'8
                        g'8
                        a'8
                    }
                >>
                \new Voice
                {
                    \oneVoice
                    c''4
                    a'4
                }
            }

        >>> for leaf in abjad.select.leaves(staff):
        ...     command = abjad.get.effective(leaf, abjad.VoiceNumber)
        ...     print(f"{leaf}, {command}")
        Note("g'8"), VoiceNumber(n=1, leak=False)
        Note("a'8"), VoiceNumber(n=1, leak=False)
        Note("b'8"), VoiceNumber(n=1, leak=False)
        Note("c''8"), VoiceNumber(n=1, leak=False)
        Note("e'8"), VoiceNumber(n=2, leak=False)
        Note("f'8"), VoiceNumber(n=2, leak=False)
        Note("g'8"), VoiceNumber(n=2, leak=False)
        Note("a'8"), VoiceNumber(n=2, leak=False)
        Note("c''4"), VoiceNumber(n=None, leak=False)
        Note("a'4"), VoiceNumber(n=None, leak=False)

    """

    n: int | None = None
    leak: bool = dataclasses.field(default=False, compare=False)

    check_effective_context: typing.ClassVar[bool] = True
    context: typing.ClassVar[str] = "Voice"
    parameter: typing.ClassVar[str] = "VOICE_NUMBER"
    persistent: typing.ClassVar[bool] = True
    temporarily_do_not_check: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert self.n in (1, 2, 3, 4, None), repr(self.n)
        assert isinstance(self.leak, bool), repr(self.leak)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        string = self._get_lilypond_format()
        if self.leak:
            contributions.after.leak.append(_EMPTY_CHORD)
            contributions.after.leaks.append(string)
        else:
            contributions.before.commands.append(string)
        return contributions

    def _get_lilypond_format(self):
        if self.n == 1:
            string = r"\voiceOne"
        elif self.n == 2:
            string = r"\voiceTwo"
        elif self.n == 3:
            string = r"\voiceThree"
        elif self.n == 4:
            string = r"\voiceFour"
        else:
            assert self.n is None
            string = r"\oneVoice"
        return string
