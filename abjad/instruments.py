r"""
Instruments.

..  container:: example

    Default ranges of each instrument:

    >>> names = [_ for _ in dir(abjad.instruments) if _[0].isupper()]
    >>> for name in names:
    ...     class_ = abjad.__dict__[name]
    ...     if issubclass(class_, abjad.Instrument):
    ...         instrument = class_()
    ...         instrument_name = instrument.__class__.__name__
    ...         range_string = instrument.pitch_range.range_string
    ...         print(f"{instrument_name}: {range_string}")
    Accordion: [E1, C8]
    AltoFlute: [G3, G6]
    AltoSaxophone: [Db3, A5]
    AltoTrombone: [A2, Bb5]
    AltoVoice: [F3, G5]
    BaritoneSaxophone: [C2, Ab4]
    BaritoneVoice: [A2, A4]
    BassClarinet: [Bb1, G5]
    BassFlute: [C3, C6]
    BassSaxophone: [Ab2, E4]
    BassTrombone: [C2, F4]
    BassVoice: [E2, F4]
    Bassoon: [Bb1, Eb5]
    Cello: [C2, G5]
    ClarinetInA: [Db3, A6]
    ClarinetInBFlat: [D3, Bb6]
    ClarinetInEFlat: [F3, C7]
    Contrabass: [C1, G4]
    ContrabassClarinet: [Bb0, G4]
    ContrabassFlute: [G2, G5]
    ContrabassSaxophone: [C1, Ab3]
    Contrabassoon: [Bb0, Bb4]
    EnglishHorn: [E3, C6]
    Flute: [C4, D7]
    FrenchHorn: [B1, F5]
    Glockenspiel: [G5, C8]
    Guitar: [E2, E5]
    Harp: [B0, G#7]
    Harpsichord: [C2, C7]
    Instrument: [-inf, +inf]
    Marimba: [F2, C7]
    MezzoSopranoVoice: [A3, C6]
    Oboe: [Bb3, A6]
    Percussion: [-inf, +inf]
    Piano: [A0, C8]
    Piccolo: [D5, C8]
    SopraninoSaxophone: [Db4, F#6]
    SopranoSaxophone: [Ab3, E6]
    SopranoVoice: [C4, E6]
    TenorSaxophone: [Ab2, E5]
    TenorTrombone: [E2, Eb5]
    TenorVoice: [C3, D5]
    Trumpet: [F#3, D6]
    Tuba: [D1, F4]
    Vibraphone: [F3, F6]
    Viola: [C3, D6]
    Violin: [G3, G7]
    Xylophone: [C4, C7]

..  container:: example

    Two instruments active on a single staff:

    >>> voice_1 = abjad.Voice("e'8 g'8 f'8 a'8")
    >>> voice_2 = abjad.Voice("c'2")
    >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    >>> flute = abjad.Flute()
    >>> abjad.attach(flute, voice_1[0], context="Voice")
    >>> abjad.attach(abjad.VoiceNumber(1), voice_1[0])
    >>> abjad.attach(abjad.VoiceNumber(2), voice_2[0])
    >>> viola = abjad.Viola()
    >>> abjad.attach(viola, voice_2[0], context="Voice")
    >>> abjad.show(staff) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        <<
            \new Voice
            {
                \voiceOne
                e'8
                g'8
                f'8
                a'8
            }
            \new Voice
            {
                \voiceTwo
                c'2
            }
        >>

    >>> for leaf in abjad.select.leaves(voice_1):
    ...     leaf, abjad.get.effective(leaf, abjad.Instrument)
    ...
    (Note("e'8"), Flute(clefs=('treble',), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C4, D7]')))
    (Note("g'8"), Flute(clefs=('treble',), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C4, D7]')))
    (Note("f'8"), Flute(clefs=('treble',), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C4, D7]')))
    (Note("a'8"), Flute(clefs=('treble',), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C4, D7]')))

    >>> for leaf in abjad.select.leaves(voice_2):
    ...     leaf, abjad.get.effective(leaf, abjad.Instrument)
    ...
    (Note("c'2"), Viola(clefs=('alto', 'treble'), context='Staff', middle_c_sounding_pitch=NamedPitch("c'"), pitch_range=PitchRange(range_string='[C3, D6]'), tuning=Tuning(pitches=(NamedPitch('c'), NamedPitch('g'), NamedPitch("d'"), NamedPitch("a'")))))

"""

import dataclasses
import typing

from . import contributions as _contributions
from . import enumerate as _enumerate
from . import pcollections as _pcollections
from . import pitch as _pitch


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Instrument:
    """
    Instrument.
    """

    clefs: tuple[str, ...] = ()
    context: str = "Staff"
    # find_context_on_attach: typing.ClassVar[bool] = True
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[-inf, +inf]")

    check_effective_context: typing.ClassVar[bool] = True
    latent: typing.ClassVar[bool] = True
    persistent: typing.ClassVar[bool] = True
    redraw: typing.ClassVar[bool] = True
    site: typing.ClassVar[str] = "before"

    def __post_init__(self):
        assert isinstance(self.context, str), repr(self.context)
        assert isinstance(self.clefs, tuple), repr(self.clefs)
        assert all(isinstance(_, str) for _ in self.clefs)
        assert isinstance(self.pitch_range, _pcollections.PitchRange), repr(
            self.pitch_range
        )
        assert isinstance(self.middle_c_sounding_pitch, _pitch.NamedPitch), repr(
            self.middle_c_sounding_pitch
        )

    @property
    def _lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__

    def _attachment_test_all(self, leaf):
        assert hasattr(leaf, "written_duration")
        if leaf._has_indicator(Instrument):
            string = f"Already has instrument: {leaf}."
            return string
        return True

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        site = getattr(contributions, self.site)
        strings = self._get_lilypond_format()
        assert isinstance(strings, list), repr(strings)
        site.commands.extend(strings)
        return contributions

    def _get_lilypond_format(self, context=None):
        return []


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StringNumber:
    """
    String number.

    ..  container:: example

        String I:

        >>> abjad.StringNumber((1,))
        StringNumber(numbers=(1,))

        Strings II and III:

        >>> abjad.StringNumber((2, 3))
        StringNumber(numbers=(2, 3))

    """

    numbers: tuple[int, ...] = (1,)

    def __post_init__(self):
        assert isinstance(self.numbers, tuple), repr(self.numbers)
        assert all(0 < _ < 7 for _ in self.numbers)

    @property
    def roman_numerals(self) -> tuple[str, ...]:
        """
        Gets roman numerals of string number indicator.

        ..  container:: example

            String I:

            >>> indicator = abjad.StringNumber((1,))
            >>> indicator.roman_numerals
            ('i',)

            Strings II and III:

            >>> indicator = abjad.StringNumber((2, 3))
            >>> indicator.roman_numerals
            ('ii', 'iii')

        """
        numerals = ("i", "ii", "iii", "iv", "v", "vi")
        result = []
        for number in self.numbers:
            numeral = numerals[number - 1]
            result.append(numeral)
        return tuple(result)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tuning:
    """
    Tuning.

    ..  container:: example

        Violin tuning:

        >>> pitches = [abjad.NamedPitch(_) for _ in "G3 D4 A4 E5".split()]
        >>> abjad.Tuning(tuple(pitches))
        Tuning(pitches=(NamedPitch('g'), NamedPitch("d'"), NamedPitch("a'"), NamedPitch("e''")))

    """

    pitches: tuple[_pitch.NamedPitch, ...] = ()

    def __post_init__(self):
        assert isinstance(self.pitches, tuple), repr(self.pitches)
        assert all(isinstance(_, _pitch.NamedPitch) for _ in self.pitches)

    @property
    def pitch_ranges(self) -> list[_pcollections.PitchRange]:
        """
        Gets two-octave pitch-ranges for each pitch in this tuning.

        ..  container:: example

            >>> pitches = [abjad.NamedPitch(_) for _ in "G3 D4 A4 E5".split()]
            >>> tuning = abjad.Tuning(tuple(pitches))
            >>> for range_ in tuning.pitch_ranges:
            ...     range_
            PitchRange(range_string='[G3, G5]')
            PitchRange(range_string='[D4, D6]')
            PitchRange(range_string='[A4, A6]')
            PitchRange(range_string='[E5, E7]')

        """
        result = []
        for pitch in self.pitches or []:
            pitch_range: _pcollections.PitchRange = _pcollections.PitchRange(
                f"[{pitch.name}, {(pitch + 24).name}]"
            )
            result.append(pitch_range)
        return result

    def get_pitch_ranges_by_string_number(
        self, string_number: StringNumber
    ) -> tuple[_pcollections.PitchRange, ...]:
        """
        Gets tuning pitch ranges by string number.

        Violin tuning:

        ..  container:: example

            >>> pitches = [abjad.NamedPitch(_) for _ in "G3 D4 A4 E5".split()]
            >>> tuning = abjad.Tuning(tuple(pitches))
            >>> string_number = abjad.StringNumber((2, 3))
            >>> tuning.get_pitch_ranges_by_string_number(string_number)
            (PitchRange(range_string='[A4, A6]'), PitchRange(range_string='[D4, D6]'))

        """
        if not isinstance(string_number, StringNumber):
            string_number = StringNumber(string_number)
        assert isinstance(string_number, StringNumber)
        pitch_ranges = self.pitch_ranges
        result = []
        for number in string_number.numbers:
            index = -number
            pitch_range: _pcollections.PitchRange = pitch_ranges[index]
            result.append(pitch_range)
        return tuple(result)

    def get_pitches_by_string_number(
        self, string_number: StringNumber
    ) -> tuple[_pitch.NamedPitch, ...]:
        """
        Gets tuning pitches by string number.

        Violin tuning:

        ..  container:: example

            >>> pitches = [abjad.NamedPitch(_) for _ in "G3 D4 A4 E5".split()]
            >>> tuning = abjad.Tuning(tuple(pitches))
            >>> string_number = abjad.StringNumber((2, 3))
            >>> tuning.get_pitches_by_string_number(string_number)
            (NamedPitch("a'"), NamedPitch("d'"))

        """
        if not isinstance(string_number, StringNumber):
            string_number = StringNumber(string_number)
        assert isinstance(string_number, StringNumber)
        assert self.pitches is not None
        result = []
        for number in string_number.numbers:
            index = -number
            pitch = self.pitches[index]
            result.append(pitch)
        return tuple(result)

    def voice_pitch_classes(
        self,
        pitch_classes: list[_pitch.NamedPitchClass],
        allow_open_strings: bool = True,
    ) -> list[tuple[_pitch.NamedPitch | None, ...]]:
        r"""
        Voices ``pitch_classes``.

        ..  container:: example

            >>> pitches = [abjad.NamedPitch(_) for _ in "G3 D4 A4 E5".split()]
            >>> tuning = abjad.Tuning(tuple(pitches))
            >>> voicings = tuning.voice_pitch_classes([abjad.NamedPitchClass('a')])
            >>> for voicing in voicings:
            ...     voicing
            ...
            (NamedPitch('a'), None, None, None)
            (None, None, None, NamedPitch("a''"))
            (None, None, None, NamedPitch("a'''"))
            (None, None, NamedPitch("a'"), None)
            (None, None, NamedPitch("a''"), None)
            (None, None, NamedPitch("a'''"), None)
            (None, NamedPitch("a'"), None, None)
            (None, NamedPitch("a''"), None, None)
            (NamedPitch("a'"), None, None, None)

            >>> pcs = [abjad.NamedPitchClass(_) for _ in ["a", "d"]]
            >>> voicings = tuning.voice_pitch_classes(pcs, allow_open_strings=False)
            >>> for voicing in voicings:
            ...     voicing
            ...
            (NamedPitch('a'), None, None, NamedPitch("d'''"))
            (NamedPitch('a'), None, None, NamedPitch("d''''"))
            (NamedPitch('a'), None, NamedPitch("d''"), None)
            (NamedPitch('a'), None, NamedPitch("d'''"), None)
            (NamedPitch('a'), NamedPitch("d''"), None, None)
            (NamedPitch('a'), NamedPitch("d'''"), None, None)
            (None, None, NamedPitch("d''"), NamedPitch("a''"))
            (None, None, NamedPitch("d''"), NamedPitch("a'''"))
            (None, None, NamedPitch("a''"), NamedPitch("d'''"))
            (None, None, NamedPitch("a''"), NamedPitch("d''''"))
            (None, None, NamedPitch("d'''"), NamedPitch("a''"))
            (None, None, NamedPitch("d'''"), NamedPitch("a'''"))
            (None, None, NamedPitch("a'''"), NamedPitch("d'''"))
            (None, None, NamedPitch("a'''"), NamedPitch("d''''"))
            (None, NamedPitch("a'"), None, NamedPitch("d'''"))
            (None, NamedPitch("a'"), None, NamedPitch("d''''"))
            (None, NamedPitch("a'"), NamedPitch("d''"), None)
            (None, NamedPitch("a'"), NamedPitch("d'''"), None)
            (None, NamedPitch("d''"), None, NamedPitch("a''"))
            (None, NamedPitch("d''"), None, NamedPitch("a'''"))
            (None, NamedPitch("d''"), NamedPitch("a''"), None)
            (None, NamedPitch("d''"), NamedPitch("a'''"), None)
            (None, NamedPitch("a''"), None, NamedPitch("d'''"))
            (None, NamedPitch("a''"), None, NamedPitch("d''''"))
            (None, NamedPitch("a''"), NamedPitch("d''"), None)
            (None, NamedPitch("a''"), NamedPitch("d'''"), None)
            (None, NamedPitch("d'''"), None, NamedPitch("a''"))
            (None, NamedPitch("d'''"), None, NamedPitch("a'''"))
            (None, NamedPitch("d'''"), NamedPitch("a''"), None)
            (None, NamedPitch("d'''"), NamedPitch("a'''"), None)
            (NamedPitch("d'"), None, None, NamedPitch("a''"))
            (NamedPitch("d'"), None, None, NamedPitch("a'''"))
            (NamedPitch("d'"), None, NamedPitch("a''"), None)
            (NamedPitch("d'"), None, NamedPitch("a'''"), None)
            (NamedPitch("d'"), NamedPitch("a'"), None, None)
            (NamedPitch("d'"), NamedPitch("a''"), None, None)
            (NamedPitch("a'"), None, None, NamedPitch("d'''"))
            (NamedPitch("a'"), None, None, NamedPitch("d''''"))
            (NamedPitch("a'"), None, NamedPitch("d''"), None)
            (NamedPitch("a'"), None, NamedPitch("d'''"), None)
            (NamedPitch("a'"), NamedPitch("d''"), None, None)
            (NamedPitch("a'"), NamedPitch("d'''"), None, None)
            (NamedPitch("d''"), None, None, NamedPitch("a''"))
            (NamedPitch("d''"), None, None, NamedPitch("a'''"))
            (NamedPitch("d''"), None, NamedPitch("a''"), None)
            (NamedPitch("d''"), None, NamedPitch("a'''"), None)
            (NamedPitch("d''"), NamedPitch("a'"), None, None)
            (NamedPitch("d''"), NamedPitch("a''"), None, None)

        """
        assert self.pitches is not None
        assert all(isinstance(_, _pitch.NamedPitchClass) for _ in pitch_classes), repr(
            pitch_classes
        )
        nones = [None] * (len(self.pitches) - len(pitch_classes))
        pcs_and_nones = pitch_classes + nones
        permutations = _enumerate.yield_permutations(pcs_and_nones)
        unique_tuples = set([tuple(_) for _ in permutations])
        pitch_ranges = self.pitch_ranges
        result: list[tuple[_pitch.NamedPitch | None, ...]] = []
        for permutation in unique_tuples:
            sequences: list = []
            for pitch_range, pitch_class in zip(pitch_ranges, permutation):
                pitches: list[_pitch.NamedPitch | None]
                if pitch_class is None:
                    sequences.append([None])
                    continue
                pitches = list(pitch_range.voice_pitch_class(pitch_class))
                if not allow_open_strings:
                    pitches = [
                        pitch for pitch in pitches if pitch != pitch_range.start_pitch
                    ]
                if not pitches:
                    pitches = [None]
                sequences.append(pitches)
            subresult = _enumerate.outer_product(sequences)
            subresult = [tuple(x) for x in subresult]
            result.extend(subresult)
        assert isinstance(result, list)
        assert all(isinstance(_, tuple) for _ in result)
        result.sort()
        return result


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Accordion(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "StaffGroup"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[E1, C8]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AltoFlute(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("G3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[G3, G6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AltoSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Eb3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Db3, A5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AltoTrombone(Instrument):
    clefs: tuple[str, ...] = ("bass", "tenor")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[A2, Bb5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AltoVoice(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[F3, G5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BaritoneSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Eb2")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C2, Ab4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BaritoneVoice(Instrument):
    clefs: tuple[str, ...] = ("bass",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[A2, A4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BassClarinet(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Bb2")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Bb1, G5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BassFlute(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C3, C6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BassSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Bb1")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Ab2, E4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BassTrombone(Instrument):
    clefs: tuple[str, ...] = ("bass",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C2, F4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BassVoice(Instrument):
    clefs: tuple[str, ...] = ("bass",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[E2, F4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Bassoon(Instrument):
    clefs: tuple[str, ...] = ("bass", "tenor")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Bb1, Eb5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Cello(Instrument):
    clefs: tuple[str, ...] = ("bass", "tenor", "treble")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C2, G5]")
    tuning: Tuning = Tuning(
        tuple([_pitch.NamedPitch(_) for _ in "C2 G2 D3 A3".split()])
    )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ClarinetInA(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("A3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Db3, A6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ClarinetInBFlat(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Bb3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[D3, Bb6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ClarinetInEFlat(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Eb4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[F3, C7]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Contrabass(Instrument):
    clefs: tuple[str, ...] = ("bass", "treble")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C1, G4]")
    tuning: Tuning = Tuning(
        tuple([_pitch.NamedPitch(_) for _ in "C1 A1 D2 G2".split()])
    )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ContrabassClarinet(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Bb1")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Bb0, G4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ContrabassFlute(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("G2")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[G2, G5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ContrabassSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Eb1")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C1, Ab3]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Contrabassoon(Instrument):
    clefs: tuple[str, ...] = ("bass",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Bb0, Bb4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class EnglishHorn(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("F3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[E3, C6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Flute(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C4, D7]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class FrenchHorn(Instrument):
    clefs: tuple[str, ...] = ("bass", "treble")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("F3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[B1, F5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Glockenspiel(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C6")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[G5, C8]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Guitar(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[E2, E5]")
    tuning: Tuning = Tuning(
        tuple([_pitch.NamedPitch(_) for _ in "E2 A2 D3 G3 B3 E4".split()])
    )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Harp(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "StaffGroup"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[B0, G#7]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Harpsichord(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "StaffGroup"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C2, C7]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Marimba(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[F2, C7]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class MezzoSopranoVoice(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[A3, C6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Oboe(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Bb3, A6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Percussion(Instrument):
    clefs: tuple[str, ...] = ("percussion",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[-inf, +inf]")

    known_percussion = tuple(
        sorted(
            set(
                [
                    "agogô",
                    "anvil",
                    "bass drum",
                    "bongo drums",
                    "cabasa",
                    "cajón",
                    "castanets",
                    "caxixi",
                    "claves",
                    "conga drums",
                    "cowbell",
                    "crotales",
                    "cuíca",
                    "djembe",
                    "finger cymbals",
                    "flexatone",
                    "frame drum",
                    "gong",
                    "güiro",
                    "hand-held stones",
                    "jawbone",
                    "maracas",
                    "ratchet",
                    "rattle",
                    "sand blocks",
                    "scraped slate",
                    "siren",
                    "slapstick",
                    "slide whistle",
                    "snare drum",
                    "sponges",
                    "suspended cymbal",
                    "steel drums",
                    "tam-tam",
                    "tambourine",
                    "temple blocks",
                    "thunder machine",
                    "thundersheet",
                    "toms",
                    "tubular bells",
                    "triangle",
                    "vibraslap",
                    "whistle",
                    "wind chime",
                    "wind machine",
                    "wood blocks",
                    "wood planks",
                ]
            )
        )
    )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Piano(Instrument):
    clefs: tuple[str, ...] = ("treble", "bass")
    context: str = "StaffGroup"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[A0, C8]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Piccolo(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C5")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[D5, C8]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class SopraninoSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Eb4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Db4, F#6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class SopranoSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Bb3")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Ab3, E6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class SopranoVoice(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C4, E6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class TenorSaxophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("Bb2")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[Ab2, E5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class TenorTrombone(Instrument):
    clefs: tuple[str, ...] = ("tenor", "bass")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[E2, Eb5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class TenorVoice(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C3, D5]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Trumpet(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[F#3, D6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tuba(Instrument):
    clefs: tuple[str, ...] = ("bass",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[D1, F4]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Vibraphone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[F3, F6]")


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Viola(Instrument):
    clefs: tuple[str, ...] = ("alto", "treble")
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C3, D6]")
    tuning: Tuning = Tuning(
        tuple([_pitch.NamedPitch(_) for _ in "C3 G3 D4 A4".split()])
    )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Violin(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C4")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[G3, G7]")
    tuning: Tuning = Tuning(
        tuple([_pitch.NamedPitch(_) for _ in "G3 D4 A4 E5".split()])
    )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Xylophone(Instrument):
    clefs: tuple[str, ...] = ("treble",)
    context: str = "Staff"
    middle_c_sounding_pitch: _pitch.NamedPitch = _pitch.NamedPitch("C5")
    pitch_range: _pcollections.PitchRange = _pcollections.PitchRange("[C4, C7]")
