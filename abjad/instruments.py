"""
Instrument classes.
"""
import copy
import dataclasses
import typing

from . import enumerate as _enumerate
from . import markups as _markups
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import string as _string


class Instrument:
    r"""
    Instrument.

    ..  container:: example

        Two instruments active on a single staff:

        >>> voice_1 = abjad.Voice("e'8 g'8 f'8 a'8")
        >>> flute = abjad.Flute()
        >>> abjad.attach(flute, voice_1[0], context='Voice')
        >>> flute_markup = abjad.Markup(r'\markup (flute)', direction=abjad.Up)
        >>> abjad.attach(flute_markup, voice_1[0])
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
        >>> voice_2 = abjad.Voice("c'2")
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
        >>> viola = abjad.Viola()
        >>> abjad.attach(viola, voice_2[0], context='Voice')
        >>> viola_markup = abjad.Markup(r'\markup (viola)', direction=abjad.Down)
        >>> abjad.attach(viola_markup, voice_2[0])
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
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
                    ^ \markup (flute)
                    g'8
                    f'8
                    a'8
                }
                \new Voice
                {
                    \voiceTwo
                    c'2
                    _ \markup (viola)
                }
            >>

        >>> for leaf in abjad.select.leaves(voice_1):
        ...     leaf, abjad.get.effective(leaf, abjad.Instrument)
        ...
        (Note("e'8"), Flute())
        (Note("g'8"), Flute())
        (Note("f'8"), Flute())
        (Note("a'8"), Flute())

        >>> for leaf in abjad.select.leaves(voice_2):
        ...     leaf, abjad.get.effective(leaf, abjad.Instrument)
        ...
        (Note("c'2"), Viola())

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allowable_clefs",
        "_context",
        "_middle_c_sounding_pitch",
        "_name",
        "_name_markup",
        "_primary",
        "_middle_c_sounding_pitch",
        "_performer_names",
        "_pitch_range",
        "_short_name",
        "_short_name_markup",
        "_starting_clefs",
    )

    _format_slot = "opening"

    _latent = True

    _persistent = True

    _redraw = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allowable_clefs=None,
        context=None,
        markup=None,
        middle_c_sounding_pitch=None,
        name=None,
        pitch_range=None,
        primary=None,
        short_name=None,
        short_markup=None,
    ):
        self._context = context or "Staff"
        if name is not None:
            name = str(name)
        self._name = name
        if markup is not None:
            markup = _markups.Markup(str(markup))
        self._name_markup = markup
        if short_name is not None:
            short_name = str(short_name)
        self._short_name = short_name
        if short_markup is not None:
            short_markup = _markups.Markup(str(short_markup))
        self._short_name_markup = short_markup
        allowable_clefs = allowable_clefs or ("treble",)
        self._allowable_clefs = allowable_clefs
        if isinstance(pitch_range, str):
            pitch_range = _pcollections.PitchRange(pitch_range)
        elif isinstance(pitch_range, _pcollections.PitchRange):
            pitch_range = copy.copy(pitch_range)
        elif pitch_range is None:
            pitch_range = _pcollections.PitchRange()
        else:
            raise TypeError(pitch_range)
        self._pitch_range = pitch_range
        middle_c_sounding_pitch = middle_c_sounding_pitch or _pitch.NamedPitch("c'")
        middle_c_sounding_pitch = _pitch.NamedPitch(middle_c_sounding_pitch)
        self._middle_c_sounding_pitch = middle_c_sounding_pitch
        if primary is not None:
            primary = bool(primary)
        self._primary = primary
        self._performer_names = ["instrumentalist"]
        self._starting_clefs = copy.copy(allowable_clefs)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Compares all nine initializer parameters.
        """
        if isinstance(argument, type(self)):
            return (
                self.allowable_clefs == argument.allowable_clefs
                and self.context == argument.context
                and self.markup == argument.markup
                and self.middle_c_sounding_pitch == argument.middle_c_sounding_pitch
                and self.name == argument.name
                and self.pitch_range == argument.pitch_range
                and self.primary == argument.primary
                and self.short_name == argument.short_name
                and self.short_markup == argument.short_markup
            )
        return False

    def __hash__(self) -> int:
        """
        Hashes instrument.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}()"

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, leaf):
        assert hasattr(leaf, "written_duration")
        if leaf._has_indicator(Instrument):
            string = f"Already has instrument: {leaf}."
            return string
        return True

    def _get_lilypond_format(self, context=None):
        return []

    def _initialize_default_name_markups(self):
        if self._name_markup is None:
            if self.name:
                string = self.name
                string = _string.capitalize_start(string)
                markup = _markups.Markup(rf"\markup {string}")
                self._name_markup = markup
            else:
                self._name_markup = None
        if self._short_name_markup is None:
            if self.short_name:
                string = self.short_name
                string = _string.capitalize_start(string)
                markup = _markups.Markup(rf"\markup {string}")
            else:
                self._short_name_markup = None

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        """
        Gets allowable clefs.

        Returns clef list.
        """
        if self._allowable_clefs is None:
            self._allowable_clefs = ("treble",)
        return self._allowable_clefs

    @property
    def context(self):
        """
        Gets (historically conventional) context of instrument.

        Defaults to ``'Staff'``.

        Returns lilypond type of context.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def latent(self):
        """
        Is true for all instruments.

        Class constant.

        Returns true.
        """
        return self._latent

    @property
    def markup(self):
        """
        Gets instrument name markup.

        Returns markup.
        """
        if self._name_markup is None:
            self._initialize_default_name_markups()
        if self._name_markup is None:
            return
        if not isinstance(self._name_markup, _markups.Markup):
            assert isinstance(self._name_markup, str), repr(self._name_markup)
            markup = _markups.Markup(rf"\markup {self._name_markup}")
            self._name_markup = markup
        if self._name_markup.string:
            return self._name_markup

    @property
    def middle_c_sounding_pitch(self):
        """
        Gets sounding pitch of written middle C.

        Returns named pitch.
        """
        return self._middle_c_sounding_pitch

    @property
    def name(self):
        """
        Gets instrument name.

        Returns string.
        """
        return self._name

    @property
    def persistent(self) -> bool:
        """
        Is true.

        Class constant.
        """
        return self._persistent

    @property
    def pitch_range(self):
        """
        Gets pitch range.

        Returns pitch range.
        """
        return self._pitch_range

    @property
    def primary(self):
        """
        Is true when instrument is historically conventional primary instrument
        (eg, flute) rather than doubling (eg, piccolo).
        """
        return self._primary

    @property
    def redraw(self):
        """
        Is true for all instruments.

        Class constant.

        Returns true.
        """
        return self._redraw

    @property
    def short_markup(self):
        """
        Gets short instrument name markup.

        Returns markup.
        """
        if self._short_name_markup is None:
            self._initialize_default_name_markups()
        if self._short_name_markup is None:
            return
        if not isinstance(self._short_name_markup, _markups.Markup):
            assert isinstance(self._short_name_markup, str), repr(
                self._short_name_markup
            )
            markup = _markups.Markup(rf"\markup {self._short_name_markup}")
            self._short_name_markup = markup
        if self._short_name_markup.string:
            return self._short_name_markup

    @property
    def short_name(self):
        """
        Gets short instrument name.

        Returns string.
        """
        return self._short_name


@dataclasses.dataclass(slots=True)
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

    numbers: typing.Iterable[int]

    def __post_init__(self):
        numbers_ = tuple(self.numbers)
        assert isinstance(numbers_, tuple), repr(numbers_)
        numbers_ = tuple(int(_) for _ in numbers_)
        assert all(0 < _ < 7 for _ in numbers_)
        self.numbers = numbers_

    @property
    def roman_numerals(self) -> typing.Tuple[str, ...]:
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


@dataclasses.dataclass(slots=True)
class Tuning:
    """
    Tuning.

    ..  container:: example

        Violin tuning:

        >>> abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
        Tuning(pitches=PitchSegment(items="g d' a' e''", item_class=NamedPitch))

    """

    pitches: typing.Sequence

    def __post_init__(self):
        if isinstance(self.pitches, type(self)):
            self.pitches = self.pitches.pitches
        self.pitches = _pcollections.PitchSegment(
            items=self.pitches, item_class=_pitch.NamedPitch
        )

    def __hash__(self):
        """
        Hashes tuning.
        """
        return hash(repr(self))

    @property
    def pitch_ranges(self) -> typing.List[_pcollections.PitchRange]:
        """
        Gets two-octave pitch-ranges for each pitch in this tuning.

        ..  container:: example

            >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
            >>> for range_ in indicator.pitch_ranges:
            ...     range_
            PitchRange(range_string='[G3, G5]')
            PitchRange(range_string='[D4, D6]')
            PitchRange(range_string='[A4, A6]')
            PitchRange(range_string='[E5, E7]')

        """
        result = []
        for pitch in self.pitches or []:
            pitch_range = _pcollections.PitchRange(f"[{pitch}, {pitch + 24}]")
            result.append(pitch_range)
        return result

    def get_pitch_ranges_by_string_number(
        self, string_number: StringNumber
    ) -> typing.Tuple[_pcollections.PitchRange, ...]:
        """
        Gets tuning pitch ranges by string number.

        ..  container:: example

            Violin tuning:

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
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
            pitch_range = pitch_ranges[index]
            result.append(pitch_range)
        return tuple(result)

    def get_pitches_by_string_number(
        self, string_number: StringNumber
    ) -> typing.Tuple[_pitch.NamedPitch, ...]:
        """
        Gets tuning pitches by string number.

        ..  container:: example

            Violin tuning:

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
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

    def voice_pitch_classes(self, pitch_classes, allow_open_strings: bool = True):
        r"""
        Voices ``pitch_classes``.

        ..  container:: example

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
            >>> voicings = tuning.voice_pitch_classes(('a',))
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

            >>> voicings = tuning.voice_pitch_classes(
            ...     ('a', 'd'),
            ...     allow_open_strings=False,
            ...     )
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
        pitch_classes = [_pitch.NamedPitchClass(_) for _ in pitch_classes]
        pitch_classes.extend([None] * (len(self.pitches) - len(pitch_classes)))
        permutations = _enumerate.yield_permutations(pitch_classes)
        permutations = set([tuple(_) for _ in permutations])
        pitch_ranges = self.pitch_ranges
        result: typing.List[
            typing.Tuple[typing.Union[_pitch.NamedPitch, None], ...]
        ] = []
        for permutation in permutations:
            sequences: typing.List = []
            for pitch_range, pitch_class in zip(pitch_ranges, permutation):
                pitches: typing.List[typing.Optional[_pitch.NamedPitch]]
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
        result.sort()
        return tuple(result)


class Accordion(Instrument):
    r"""
    Accordion.

    ..  container:: example

        >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
        >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(abjad.Staff("c'2 b2"))
        >>> accordion = abjad.Accordion()
        >>> abjad.attach(accordion, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
                    \clef "bass"
                    c'2
                    b2
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allowable_clefs=("treble", "bass"),
        context="StaffGroup",
        name="accordion",
        markup=None,
        middle_c_sounding_pitch=None,
        pitch_range="[E1, C8]",
        primary=True,
        short_markup=None,
        short_name="acc.",
    ):
        Instrument.__init__(
            self,
            allowable_clefs=allowable_clefs,
            context=context,
            name=name,
            markup=markup,
            short_markup=short_markup,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            short_name=short_name,
        )


class AltoFlute(Instrument):
    r"""
    Alto flute.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> alto_flute = abjad.AltoFlute()
        >>> abjad.attach(alto_flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="alto flute",
        short_name="alt. fl.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="G3",
        pitch_range="[G3, G6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class AltoSaxophone(Instrument):
    r"""
    Alto saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> alto_saxophone = abjad.AltoSaxophone()
        >>> abjad.attach(alto_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="alto saxophone",
        short_name="alt. sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Eb3",
        pitch_range="[Db3, A5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class AltoTrombone(Instrument):
    r"""
    Alto trombone.

    ..  container:: example

        >>> staff = abjad.Staff("c4 d4 e4 fs4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> alto_trombone = abjad.AltoTrombone()
        >>> abjad.attach(alto_trombone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c4
                d4
                e4
                fs4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="alto trombone",
        short_name="alt. trb.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass", "tenor"),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[A2, Bb5]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class AltoVoice(Instrument):
    r"""
    Alto voice.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> alto = abjad.AltoVoice()
        >>> abjad.attach(alto, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = "alto"

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="alto",
        short_name="alto",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[F3, G5]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BaritoneSaxophone(Instrument):
    r"""
    Baritone saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> baritone_saxophone = abjad.BaritoneSaxophone()
        >>> abjad.attach(baritone_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="baritone saxophone",
        short_name="bar. sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Eb2",
        pitch_range="[C2, Ab4]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BaritoneVoice(Instrument):
    r"""
    Baritone voice.

    ..  container:: example

        >>> staff = abjad.Staff("c4 d4 e4 fs4")
        >>> baritone = abjad.BaritoneVoice()
        >>> abjad.attach(baritone, staff[0])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c4
                d4
                e4
                fs4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = "bar."

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="baritone",
        short_name="bar.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass",),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[A2, A4]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BassClarinet(Instrument):
    r"""
    Bass clarinet.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> bass_clarinet = abjad.BassClarinet()
        >>> abjad.attach(bass_clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="bass clarinet",
        short_name="bass cl.",
        markup=None,
        short_markup=None,
        allowable_clefs=("treble", "bass"),
        context=None,
        middle_c_sounding_pitch="Bb2",
        pitch_range="[Bb1, G5]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BassFlute(Instrument):
    r"""
    Bass flute.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> bass_flute = abjad.BassFlute()
        >>> abjad.attach(bass_flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="bass flute",
        short_name="bass fl.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="C3",
        pitch_range="[C3, C6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BassSaxophone(Instrument):
    r"""
    Bass saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> bass_saxophone = abjad.BassSaxophone()
        >>> abjad.attach(bass_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="bass saxophone",
        short_name="bass sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Bb1",
        pitch_range="[Ab2, E4]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BassTrombone(Instrument):
    r"""
    Bass trombone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> bass_trombone = abjad.BassTrombone()
        >>> abjad.attach(bass_trombone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="bass trombone",
        short_name="bass trb.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass",),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[C2, F4]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class BassVoice(Instrument):
    r"""
    Bass voice.

    ..  container:: example

        >>> staff = abjad.Staff("c4 d4 e4 fs4")
        >>> bass = abjad.BassVoice()
        >>> abjad.attach(bass, staff[0])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c4
                d4
                e4
                fs4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="bass",
        short_name="bass",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass",),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[E2, F4]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Bassoon(Instrument):
    r"""
    Bassoon.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> bassoon = abjad.Bassoon()
        >>> abjad.attach(bassoon, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="bassoon",
        short_name="bsn.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass", "tenor"),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[Bb1, Eb5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Cello(Instrument):
    r"""
    Cello.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> cello = abjad.Cello()
        >>> abjad.attach(cello, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_default_tuning",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="cello",
        short_name="vc.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass", "tenor", "treble"),
        context=None,
        default_tuning=("C2", "G2", "D3", "A3"),
        middle_c_sounding_pitch=None,
        pitch_range="[C2, G5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )
        self._default_tuning = Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def default_tuning(self):
        """
        Gets cello's default tuning.

        ..  container:: example

            >>> cello = abjad.Cello()
            >>> cello.default_tuning
            Tuning(pitches=PitchSegment(items="c, g, d a", item_class=NamedPitch))

        Returns tuning.
        """
        return self._default_tuning


class ClarinetInA(Instrument):
    r"""
    Clarinet in A.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = abjad.ClarinetInA()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="clarinet in A",
        short_name=r"cl. A \natural",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="A3",
        pitch_range="[Db3, A6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class ClarinetInBFlat(Instrument):
    r"""
    Clarinet in B-flat.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = abjad.ClarinetInBFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = "cl."

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="clarinet in B-flat",
        short_name="cl. in B-flat",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Bb3",
        pitch_range="[D3, Bb6]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class ClarinetInEFlat(Instrument):
    r"""
    Clarinet in E-flat.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = abjad.ClarinetInEFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="clarinet in E-flat",
        short_name="cl. E-flat",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Eb4",
        pitch_range="[F3, C7]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class Contrabass(Instrument):
    r"""
    Contrabass.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> contrabass = abjad.Contrabass()
        >>> abjad.attach(contrabass, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_default_tuning",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="contrabass",
        short_name="cb.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass", "treble"),
        context=None,
        default_tuning=("C1", "A1", "D2", "G2"),
        middle_c_sounding_pitch="C3",
        pitch_range="[C1, G4]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )
        self._default_tuning = Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def default_tuning(self):
        """
        Gets contrabass's default tuning.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.default_tuning
            Tuning(pitches=PitchSegment(items="c,, a,, d, g,", item_class=NamedPitch))

        Returns tuning.
        """
        return self._default_tuning


class ContrabassClarinet(Instrument):
    r"""
    Contrassbass clarinet.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_clarinet = abjad.ContrabassClarinet()
        >>> abjad.attach(contrabass_clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="contrabass clarinet",
        short_name="cbass. cl.",
        markup=None,
        short_markup=None,
        allowable_clefs=("treble", "bass"),
        context=None,
        middle_c_sounding_pitch="Bb1",
        pitch_range="[Bb0, G4]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class ContrabassFlute(Instrument):
    r"""
    Contrabass flute.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_flute = abjad.ContrabassFlute()
        >>> abjad.attach(contrabass_flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="contrabass flute",
        short_name="cbass. fl.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="G2",
        pitch_range="[G2, G5]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class ContrabassSaxophone(Instrument):
    r"""
    Contrabass saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_saxophone = abjad.ContrabassSaxophone()
        >>> abjad.attach(contrabass_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="contrabass saxophone",
        short_name="cbass. sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Eb1",
        pitch_range="[C1, Ab3]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class Contrabassoon(Instrument):
    r"""
    Contrabassoon.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> contrabassoon = abjad.Contrabassoon()
        >>> abjad.attach(contrabassoon, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="contrabassoon",
        short_name="contrabsn.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass",),
        context=None,
        middle_c_sounding_pitch="C3",
        pitch_range="[Bb0, Bb4]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class EnglishHorn(Instrument):
    r"""
    English horn.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> english_horn = abjad.EnglishHorn()
        >>> abjad.attach(english_horn, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="English horn",
        short_name="Eng. hn.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="F3",
        pitch_range="[E3, C6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class Flute(Instrument):
    r"""
    Flute.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> flute = abjad.Flute()
        >>> abjad.attach(flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    ..  container:: example

        Instrument markup can be hidden:

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> flute = abjad.Flute()
        >>> abjad.attach(flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            c'4
            d'4
            e'4
            fs'4
        }

        >>> for leaf in abjad.select.leaves(staff):
        ...     leaf, abjad.get.effective(leaf, abjad.Instrument)
        ...
        (Note("c'4"), Flute())
        (Note("d'4"), Flute())
        (Note("e'4"), Flute())
        (Note("fs'4"), Flute())

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="flute",
        short_name="fl.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[C4, D7]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class FrenchHorn(Instrument):
    r"""
    French horn.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> french_horn = abjad.FrenchHorn()
        >>> abjad.attach(french_horn, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="horn",
        short_name="hn.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass", "treble"),
        context=None,
        middle_c_sounding_pitch="F3",
        pitch_range="[B1, F5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Glockenspiel(Instrument):
    r"""
    Glockenspiel.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> glockenspiel = abjad.Glockenspiel()
        >>> abjad.attach(glockenspiel, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="glockenspiel",
        short_name="gkspl.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="C6",
        pitch_range="[G5, C8]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class Guitar(Instrument):
    r"""
    Guitar.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> guitar = abjad.Guitar()
        >>> abjad.attach(guitar, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_default_tuning",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="guitar",
        short_name="gt.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        default_tuning=("E2", "A2", "D3", "G3", "B3", "E4"),
        middle_c_sounding_pitch="C3",
        pitch_range="[E2, E5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )
        self._default_tuning = Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def default_tuning(self):
        """
        Gets guitar's default tuning.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.default_tuning
            Tuning(pitches=PitchSegment(items="e, a, d g b e'", item_class=NamedPitch))

        Returns tuning.
        """
        return self._default_tuning


class Harp(Instrument):
    r"""
    Harp.

    ..  container:: example

        >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
        >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(abjad.Staff("c'2 b2"))
        >>> harp = abjad.Harp()
        >>> abjad.attach(harp, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
                    \clef "bass"
                    c'2
                    b2
                }
            >>

    The harp targets piano staff context by default.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="harp",
        short_name="hp.",
        markup=None,
        short_markup=None,
        allowable_clefs=("treble", "bass"),
        context="StaffGroup",
        middle_c_sounding_pitch=None,
        pitch_range="[B0, G#7]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Harpsichord(Instrument):
    r"""
    Harpsichord.

    ..  container:: example

        >>> upper_staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> lower_staff = abjad.Staff("c'2 b2")
        >>> staff_group = abjad.StaffGroup(
        ...     [upper_staff, lower_staff],
        ...     lilypond_type='PianoStaff',
        ...     )
        >>> harpsichord = abjad.Harpsichord()
        >>> abjad.attach(harpsichord, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), lower_staff[0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
                    \clef "bass"
                    c'2
                    b2
                }
            >>

    The harpsichord targets piano staff context by default.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="harpsichord",
        short_name="hpschd.",
        markup=None,
        short_markup=None,
        allowable_clefs=("treble", "bass"),
        context="StaffGroup",
        middle_c_sounding_pitch=None,
        pitch_range="[C2, C7]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Marimba(Instrument):
    r"""
    Marimba.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> marimba = abjad.Marimba()
        >>> abjad.attach(marimba, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="marimba",
        short_name="mb.",
        markup=None,
        short_markup=None,
        allowable_clefs=("treble", "bass"),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[F2, C7]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class MezzoSopranoVoice(Instrument):
    r"""
    Mezzo-soprano voice.

    ..  container:: example


        >>> staff = abjad.Staff("c''4 d''4 e''4 fs''4")
        >>> mezzo_soprano = abjad.MezzoSopranoVoice()
        >>> abjad.attach(mezzo_soprano, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c''4
                d''4
                e''4
                fs''4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = "ms."

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="mezzo-soprano",
        short_name="mezz.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[A3, C6]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            pitch_range=pitch_range,
            primary=primary,
        )


class Oboe(Instrument):
    r"""
    Oboe.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> oboe = abjad.Oboe()
        >>> abjad.attach(oboe, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="oboe",
        short_name="ob.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[Bb3, A6]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Percussion(Instrument):
    r"""
    Percussion instrument.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> percussion = abjad.Percussion()
        >>> abjad.attach(percussion, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    known_percussion = list(
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

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="percussion",
        short_name="perc.",
        markup=None,
        short_markup=None,
        allowable_clefs=("percussion",),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range=None,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class Piano(Instrument):
    r"""
    Piano.

    ..  container:: example

        >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
        >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(abjad.Staff("c'2 b2"))
        >>> piano = abjad.Piano()
        >>> abjad.attach(piano, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new PianoStaff
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
                    \clef "bass"
                    c'2
                    b2
                }
            >>

    The piano targets piano staff context by default.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="piano",
        short_name="pf.",
        markup=None,
        short_markup=None,
        allowable_clefs=("treble", "bass"),
        context="StaffGroup",
        middle_c_sounding_pitch=None,
        pitch_range="[A0, C8]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Piccolo(Instrument):
    r"""
    Piccolo.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> piccolo = abjad.Piccolo()
        >>> abjad.attach(piccolo, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="piccolo",
        short_name="picc.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="C5",
        pitch_range="[D5, C8]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class SopraninoSaxophone(Instrument):
    r"""
    Sopranino saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> sopranino_saxophone = abjad.SopraninoSaxophone()
        >>> abjad.attach(sopranino_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="sopranino saxophone",
        short_name="sopranino sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Eb4",
        pitch_range="[Db4, F#6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class SopranoSaxophone(Instrument):
    r"""
    Soprano saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> soprano_saxophone = abjad.SopranoSaxophone()
        >>> abjad.attach(soprano_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="soprano saxophone",
        short_name="sop. sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Bb3",
        pitch_range="[Ab3, E6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class SopranoVoice(Instrument):
    r"""
    Soprano voice.

    ..  container:: example

        >>> staff = abjad.Staff("c''4 d''4 e''4 fs''4")
        >>> soprano = abjad.SopranoVoice()
        >>> abjad.attach(soprano, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c''4
                d''4
                e''4
                fs''4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = "sop."

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="soprano",
        short_name="sop.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[C4, E6]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class TenorSaxophone(Instrument):
    r"""
    Tenor saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> tenor_saxophone = abjad.TenorSaxophone()
        >>> abjad.attach(tenor_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="tenor saxophone",
        short_name="ten. sax.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="Bb2",
        pitch_range="[Ab2, E5]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class TenorTrombone(Instrument):
    r"""
    Tenor trombone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> tenor_trombone = abjad.TenorTrombone()
        >>> abjad.attach(tenor_trombone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="tenor trombone",
        short_name="ten. trb.",
        markup=None,
        short_markup=None,
        allowable_clefs=("tenor", "bass"),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[E2, Eb5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            pitch_range=pitch_range,
            primary=primary,
        )


class TenorVoice(Instrument):
    r"""
    Tenor voice.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> tenor = abjad.TenorVoice()
        >>> abjad.attach(tenor, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = "ten."

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="tenor",
        short_name="ten.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[C3, D5]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Trumpet(Instrument):
    r"""
    Trumpet.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> trumpet = abjad.Trumpet()
        >>> abjad.attach(trumpet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="trumpet",
        short_name="tp.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[F#3, D6]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Tuba(Instrument):
    r"""
    Tuba.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> tuba = abjad.Tuba()
        >>> abjad.attach(tuba, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="tuba",
        short_name="tb.",
        markup=None,
        short_markup=None,
        allowable_clefs=("bass",),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[D1, F4]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )


class Vibraphone(Instrument):
    r"""
    Vibraphone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> vibraphone = abjad.Vibraphone()
        >>> abjad.attach(vibraphone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="vibraphone",
        short_name="vibr.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range="[F3, F6]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )


class Viola(Instrument):
    r"""
    Viola.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('alto')
        >>> abjad.attach(clef, staff[0])
        >>> viola = abjad.Viola()
        >>> abjad.attach(viola, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_default_tuning",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="viola",
        short_name="va.",
        markup=None,
        short_markup=None,
        allowable_clefs=("alto", "treble"),
        context=None,
        default_tuning=("C3", "G3", "D4", "A4"),
        middle_c_sounding_pitch=None,
        pitch_range="[C3, D6]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )
        self._default_tuning = Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def default_tuning(self):
        """
        Gets viola's default tuning.

        ..  container:: example

            >>> viola = abjad.Viola()
            >>> viola.default_tuning
            Tuning(pitches=PitchSegment(items="c g d' a'", item_class=NamedPitch))

        Returns tuning.
        """
        return self._default_tuning


class Violin(Instrument):
    r"""
    Violin.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_default_tuning",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="violin",
        short_name="vn.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        default_tuning=("G3", "D4", "A4", "E5"),
        middle_c_sounding_pitch=None,
        pitch_range="[G3, G7]",
        primary=True,
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            primary=primary,
        )
        self._default_tuning = Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def default_tuning(self):
        """
        Gets violin's default tuning.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.default_tuning
            Tuning(pitches=PitchSegment(items="g d' a' e''", item_class=NamedPitch))

        Returns tuning.
        """
        return self._default_tuning


class Xylophone(Instrument):
    r"""
    Xylphone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> xylophone = abjad.Xylophone()
        >>> abjad.attach(xylophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name="xylophone",
        short_name="xyl.",
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch="C5",
        pitch_range="[C4, C7]",
    ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
        )
