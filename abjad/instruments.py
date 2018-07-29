"""
Instrument classes.
"""

import copy
import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.NamedPitchClass import NamedPitchClass
from abjad.pitch.PitchRange import PitchRange
from abjad.pitch.PitchSegment import PitchSegment
from abjad.utilities.Enumerator import Enumerator


class Instrument(AbjadValueObject):
    r"""
    Instrument.

    ..  container:: example

        Two instruments active on a single staff:

        >>> voice_1 = abjad.Voice("e'8 g'8 f'8 a'8")
        >>> flute = abjad.Flute()
        >>> abjad.attach(flute, voice_1[0], context='Voice')
        >>> flute_markup = abjad.Markup('(flute)', direction=abjad.Up)
        >>> abjad.attach(flute_markup, voice_1[0])
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
        >>> voice_2 = abjad.Voice("c'2")
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
        >>> viola = abjad.Viola()
        >>> abjad.attach(viola, voice_2[0], context='Voice')
        >>> viola_markup = abjad.Markup('(viola)', direction=abjad.Down)
        >>> abjad.attach(viola_markup, voice_2[0])
        >>> staff = abjad.Staff([voice_1, voice_2], is_simultaneous=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    e'8
                    ^ \markup { (flute) }
                    g'8
                    f'8
                    a'8
                }
                \new Voice
                {
                    \voiceTwo
                    c'2
                    _ \markup { (viola) }
                }
            >>

        >>> for leaf in abjad.select(voice_1).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Instrument)
        ...
        (Note("e'8"), Flute())
        (Note("g'8"), Flute())
        (Note("f'8"), Flute())
        (Note("a'8"), Flute())

        >>> for leaf in abjad.select(voice_2).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Instrument)
        ...
        (Note("c'2"), Viola())

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allowable_clefs',
        '_context',
        '_middle_c_sounding_pitch',
        '_name',
        '_name_markup',
        '_primary',
        '_middle_c_sounding_pitch',
        '_performer_names',
        '_pitch_range',
        '_short_name',
        '_short_name_markup',
        '_starting_clefs',
        )

    _format_slot = 'opening'

    _latent = True

    _parameter = 'INSTRUMENT'

    _publish_storage_format = True

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
        import abjad
        self._context = context or 'Staff'
        if name is not None:
            name = str(name)
        self._name = name
        if markup is not None:
            markup = abjad.Markup(markup)
        self._name_markup = markup
        if short_name is not None:
            short_name = str(short_name)
        self._short_name = short_name
        if short_markup is not None:
            short_markup = abjad.Markup(short_markup)
        self._short_name_markup = short_markup
        allowable_clefs = allowable_clefs or ('treble',)
        self._allowable_clefs = allowable_clefs
        if isinstance(pitch_range, str):
            pitch_range = abjad.PitchRange(pitch_range)
        elif isinstance(pitch_range, abjad.PitchRange):
            pitch_range = copy.copy(pitch_range)
        elif pitch_range is None:
            pitch_range = abjad.PitchRange()
        else:
            raise TypeError(pitch_range)
        self._pitch_range = pitch_range
        middle_c_sounding_pitch = (middle_c_sounding_pitch or
            abjad.NamedPitch("c'"))
        middle_c_sounding_pitch = abjad.NamedPitch(
            middle_c_sounding_pitch)
        self._middle_c_sounding_pitch = middle_c_sounding_pitch
        if primary is not None:
            primary = bool(primary)
        self._primary = primary
        self._performer_names = ['instrumentalist']
        self._starting_clefs = copy.copy(allowable_clefs)

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

    def _attachment_test_all(self, component_expression):
        import abjad
        if abjad.inspect(component_expression).has_indicator(Instrument):
            return False
        return True

    def _get_format_specification(self):
        import abjad
        keywords = []
        return abjad.FormatSpecification(
            self,
            repr_args_values=[],
            repr_is_indented=False,
            repr_kwargs_names=keywords,
            )

    def _get_lilypond_format(self, context=None):
        return []

    def _initialize_default_name_markups(self):
        import abjad
        if self._name_markup is None:
            if self.name:
                string = self.name
                string = abjad.String(string).capitalize_start()
                markup = abjad.Markup(contents=string)
                self._name_markup = markup
            else:
                self._name_markup = None
        if self._short_name_markup is None:
            if self.short_name:
                string = self.short_name
                string = abjad.String(string).capitalize_start()
                markup = abjad.Markup(contents=string)
                self._short_name_markup = markup
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
            self._allowable_clefs = ('treble',)
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
        import abjad
        if self._name_markup is None:
            self._initialize_default_name_markups()
        if not isinstance(self._name_markup, abjad.Markup):
            markup = abjad.Markup(contents=self._name_markup)
            self._name_markup = markup
        if self._name_markup.contents != ('',):
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
    def parameter(self) -> str:
        """
        Is set to ``'INSTRUMENT'`` for all instruments.

        Class constant.
        """
        return self._parameter

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
        import abjad
        if self._short_name_markup is None:
            self._initialize_default_name_markups()
        if not isinstance(
            self._short_name_markup, abjad.Markup):
            markup = abjad.Markup(contents=self._short_name_markup)
            self._short_name_markup = markup
        if self._short_name_markup.contents != ('',):
            return self._short_name_markup

    @property
    def short_name(self):
        """
        Gets short instrument name.

        Returns string.
        """
        return self._short_name

    ### PUBLIC METHODS ###

    @staticmethod
    def transpose_from_sounding_pitch(argument):
        r"""
        Transpose notes and chords in `argument` from sounding pitch
        to written pitch:

        ..  container:: example

            >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
            >>> clarinet = abjad.ClarinetInBFlat()
            >>> abjad.attach(clarinet, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <c' e' g'>4
                    d'4
                    r4
                    e'4
                }

            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <d' fs' a'>4
                    e'4
                    r4
                    fs'4
                }

        Returns none.
        """
        import abjad
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            instrument = abjad.inspect(leaf).effective(abjad.Instrument)
            if not instrument:
                continue
            sounding_pitch = instrument.middle_c_sounding_pitch
            interval = abjad.NamedPitch('C4') - sounding_pitch
            interval *= -1
            if isinstance(leaf, abjad.Note):
                pitch = leaf.written_pitch
                pitch = interval.transpose(pitch)
                leaf.written_pitch = pitch
            elif isinstance(leaf, abjad.Chord):
                pitches = [
                    interval.transpose(pitch)
                    for pitch in leaf.written_pitches
                    ]
                leaf.written_pitches = pitches

    @staticmethod
    def transpose_from_written_pitch(argument):
        r"""
        Transposes notes and chords in `argument` from sounding pitch
        to written pitch.

        ..  container:: example

            >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
            >>> clarinet = abjad.ClarinetInBFlat()
            >>> abjad.attach(clarinet, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <c' e' g'>4
                    d'4
                    r4
                    e'4
                }

            >>> abjad.Instrument.transpose_from_written_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <bf d' f'>4
                    c'4
                    r4
                    d'4
                }

        Returns none.
        """
        import abjad
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            instrument = abjad.inspect(leaf).effective(abjad.Instrument)
            if not instrument:
                continue
            sounding_pitch = instrument.middle_c_sounding_pitch
            interval = abjad.NamedPitch('C4') - sounding_pitch
            if isinstance(leaf, abjad.Note):
                written_pitch = leaf.written_pitch
                written_pitch = interval.transpose(written_pitch)
                leaf.written_pitch = written_pitch
            elif isinstance(leaf, abjad.Chord):
                pitches = [
                    interval.transpose(pitch)
                    for pitch in leaf.written_pitches
                    ]
                leaf.written_pitches = pitches


class StringNumber(AbjadValueObject):
    """
    String number.

    ..  container:: example

        String I:

        >>> indicator = abjad.StringNumber(1)
        >>> abjad.f(indicator)
        abjad.StringNumber(
            numbers=(1,),
            )

    ..  container:: example

        Strings II and III:

        >>> indicator = abjad.StringNumber((2, 3))
        >>> abjad.f(indicator)
        abjad.StringNumber(
            numbers=(2, 3),
            )

    """

    ### CLASS VARIABLES

    __slots__ = (
        '_numbers',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        numbers: typing.Union[int, typing.Iterable[int]] = None,
        ) -> None:
        if numbers is None:
            numbers_: typing.Tuple[int, ...] = ()
        elif isinstance(numbers, int):
            numbers_ = (numbers,)
        else:
            numbers_ = tuple(numbers)
        assert isinstance(numbers_, tuple), repr(numbers_)
        numbers_ = tuple(int(_) for _ in numbers_)
        assert all(0 < _ < 7 for _ in numbers_)
        self._numbers = numbers_

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self) -> typing.Tuple[int, ...]:
        """
        Gets numbers.

        ..  container:: example

            String I:

            >>> indicator = abjad.StringNumber(1)
            >>> indicator.numbers
            (1,)

            >>> indicator = abjad.StringNumber((2, 3))
            >>> indicator.numbers
            (2, 3)

        """
        return self._numbers

    @property
    def roman_numerals(self) -> typing.Tuple[str, ...]:
        """
        Gets roman numerals of string number indicator.

        ..  container:: example

            String I:

            >>> indicator = abjad.StringNumber(1)
            >>> indicator.roman_numerals
            ('i',)

        ..  container:: example

            Strings II and III:

            >>> indicator = abjad.StringNumber((2, 3))
            >>> indicator.roman_numerals
            ('ii', 'iii')

        """
        numerals = ('i', 'ii', 'iii', 'iv', 'v', 'vi')
        result = []
        for number in self.numbers:
            numeral = numerals[number - 1]
            result.append(numeral)
        return tuple(result)

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on string number.
        """
        pass


class Tuning(AbjadValueObject):
    """
    Tuning.

    ..  container:: example

        Violin tuning:

        >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
        >>> abjad.f(indicator)
        abjad.Tuning(
            pitches=abjad.PitchSegment(
                (
                    abjad.NamedPitch('g'),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("a'"),
                    abjad.NamedPitch("e''"),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitches',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pitches: typing.Union['Tuning', typing.Iterable] = None,
        ) -> None:
        if pitches is not None:
            if isinstance(pitches, type(self)):
                pitches = pitches.pitches
            pitches = PitchSegment(
                items=pitches,
                item_class=NamedPitch,
                )
        self._pitches: typing.Optional[PitchSegment] = pitches

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_ranges(self) -> typing.List[PitchRange]:
        """
        Gets two-octave pitch-ranges for each pitch in this tuning.

        ..  container:: example

            >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
            >>> for range_ in indicator.pitch_ranges:
            ...     range_
            PitchRange('[G3, G5]')
            PitchRange('[D4, D6]')
            PitchRange('[A4, A6]')
            PitchRange('[E5, E7]')

        """
        result = []
        for pitch in self.pitches or []:
            pitch_range = PitchRange.from_pitches(pitch, pitch + 24)
            result.append(pitch_range)
        return result

    @property
    def pitches(self) -> typing.Optional[PitchSegment]:
        """
        Gets pitches of tuning.

        ..  container:: example

            >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
            >>> pitches = indicator.pitches
            >>> abjad.f(pitches)
            abjad.PitchSegment(
                (
                    abjad.NamedPitch('g'),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("a'"),
                    abjad.NamedPitch("e''"),
                    ),
                item_class=abjad.NamedPitch,
                )

        """
        return self._pitches

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on tuning.
        """
        pass

    ### PUBLIC METHODS ###

    def get_pitch_ranges_by_string_number(
        self,
        string_number: StringNumber,
        ) -> typing.Tuple[PitchRange, ...]:
        """
        Gets tuning pitch ranges by string number.

        ..  container:: example

            Violin tuning:

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
            >>> string_number = abjad.StringNumber((2, 3))
            >>> tuning.get_pitch_ranges_by_string_number(string_number)
            (PitchRange('[A4, A6]'), PitchRange('[D4, D6]'))

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
        self,
        string_number: StringNumber,
        ) -> typing.Tuple[NamedPitch, ...]:
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

    def voice_pitch_classes(
        self,
        pitch_classes,
        allow_open_strings: bool = True,
        ):
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
        pitch_classes = [NamedPitchClass(_) for _ in pitch_classes]
        pitch_classes.extend([None] * (len(self.pitches) - len(pitch_classes)))
        enumerator = Enumerator(pitch_classes)
        permutations = enumerator.yield_permutations()
        permutations = set([tuple(_) for _ in permutations])
        pitch_ranges = self.pitch_ranges
        result: typing.List[
            typing.Tuple[typing.Union[NamedPitch, None], ...]
            ] = []
        for permutation in permutations:
            sequences = []
            for pitch_range, pitch_class in zip(pitch_ranges, permutation):
                if pitch_class is None:
                    sequences.append([None])
                    continue
                pitches = pitch_range.voice_pitch_class(pitch_class)
                if not allow_open_strings:
                    pitches = [
                        pitch for pitch in pitches
                        if pitch != pitch_range.start_pitch
                        ]
                if not pitches:
                    pitches = [None]
                sequences.append(pitches)
            enumerator = Enumerator(sequences)
            subresult = enumerator.yield_outer_product()
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

            >>> abjad.f(staff_group)
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
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        name='accordion',
        markup=None,
        middle_c_sounding_pitch=None,
        pitch_range='[E1, C8]',
        primary=True,
        short_markup=None,
        short_name='acc.',
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

            >>> abjad.f(staff)
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
        name='alto flute',
        short_name='alt. fl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='G3',
        pitch_range='[G3, G6]',
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

            >>> abjad.f(staff)
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
        name='alto saxophone',
        short_name='alt. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb3',
        pitch_range='[Db3, A5]',
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

            >>> abjad.f(staff)
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
        name='alto trombone',
        short_name='alt. trb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass', 'tenor'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[A2, Bb5]',
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

            >>> abjad.f(staff)
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

    performer_abbreviation = 'alto'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='alto',
        short_name='alto',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F3, G5]',
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

            >>> abjad.f(staff)
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
        name='baritone saxophone',
        short_name='bar. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb2',
        pitch_range='[C2, Ab4]',
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

            >>> abjad.f(staff)
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

    performer_abbreviation = 'bar.'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='baritone',
        short_name='bar.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[A2, A4]',
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

            >>> abjad.f(staff)
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
        name='bass clarinet',
        short_name='bass cl.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context=None,
        middle_c_sounding_pitch='Bb2',
        pitch_range='[Bb1, G5]',
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

            >>> abjad.f(staff)
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
        name='bass flute',
        short_name='bass fl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='C3',
        pitch_range='[C3, C6]',
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

            >>> abjad.f(staff)
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
        name='bass saxophone',
        short_name='bass sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb1',
        pitch_range='[Ab2, E4]',
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

            >>> abjad.f(staff)
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
        name='bass trombone',
        short_name='bass trb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C2, F4]',
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

            >>> abjad.f(staff)
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
        name='bass',
        short_name='bass',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[E2, F4]',
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

            >>> abjad.f(staff)
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
        name='bassoon',
        short_name='bsn.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass', 'tenor'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[Bb1, Eb5]',
        primary=True
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

            >>> abjad.f(staff)
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

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='cello',
        short_name='vc.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass', 'tenor', 'treble'),
        context=None,
        default_tuning=('C2', 'G2', 'D3', 'A3'),
        middle_c_sounding_pitch=None,
        pitch_range='[C2, G5]',
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
            Tuning(pitches=PitchSegment(['c,', 'g,', 'd', 'a']))

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

            >>> abjad.f(staff)
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
        name='clarinet in A',
        short_name=r'cl. A \natural',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='A3',
        pitch_range='[Db3, A6]',
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

            >>> abjad.f(staff)
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

    performer_abbreviation = 'cl.'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='clarinet in B-flat',
        short_name='cl. in B-flat',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb3',
        pitch_range='[D3, Bb6]',
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

            >>> abjad.f(staff)
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
        name='clarinet in E-flat',
        short_name='cl. E-flat',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb4',
        pitch_range='[F3, C7]',
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

            >>> abjad.f(staff)
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

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='contrabass',
        short_name='cb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass', 'treble'),
        context=None,
        default_tuning=('C1', 'A1', 'D2', 'G2'),
        middle_c_sounding_pitch='C3',
        pitch_range='[C1, G4]',
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
            Tuning(pitches=PitchSegment(['c,,', 'a,,', 'd,', 'g,']))

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

            >>> abjad.f(staff)
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
        name='contrabass clarinet',
        short_name='cbass. cl.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context=None,
        middle_c_sounding_pitch='Bb1',
        pitch_range='[Bb0, G4]',
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

            >>> abjad.f(staff)
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
        name='contrabass flute',
        short_name='cbass. fl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='G2',
        pitch_range='[G2, G5]',
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

            >>> abjad.f(staff)
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
        name='contrabass saxophone',
        short_name='cbass. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb1',
        pitch_range='[C1, Ab3]',
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

            >>> abjad.f(staff)
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
        name='contrabassoon',
        short_name='contrabsn.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch='C3',
        pitch_range='[Bb0, Bb4]',
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

            >>> abjad.f(staff)
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
        name='English horn',
        short_name='Eng. hn.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='F3',
        pitch_range='[E3, C6]',
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

            >>> abjad.f(staff)
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

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            fs'4
        }

        >>> for leaf in abjad.select(staff).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Instrument)
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
        name='flute',
        short_name='fl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C4, D7]',
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

            >>> abjad.f(staff)
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
        name='horn',
        short_name='hn.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass', 'treble'),
        context=None,
        middle_c_sounding_pitch='F3',
        pitch_range='[B1, F5]',
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

            >>> abjad.f(staff)
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
        name='glockenspiel',
        short_name='gkspl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='C6',
        pitch_range='[G5, C8]',
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

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='guitar',
        short_name='gt.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        default_tuning=('E2', 'A2', 'D3', 'G3', 'B3', 'E4'),
        middle_c_sounding_pitch='C3',
        pitch_range='[E2, E5]',
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
            Tuning(pitches=PitchSegment(['e,', 'a,', 'd', 'g', 'b', "e'"]))

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

            >>> abjad.f(staff_group)
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
        name='harp',
        short_name='hp.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[B0, G#7]',
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

            >>> abjad.f(staff_group)
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
        name='harpsichord',
        short_name='hpschd.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[C2, C7]',
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

            >>> abjad.f(staff)
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
        name='marimba',
        short_name='mb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F2, C7]',
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

            >>> abjad.f(staff)
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

    performer_abbreviation = 'ms.'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='mezzo-soprano',
        short_name='mezz.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[A3, C6]',
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

            >>> abjad.f(staff)
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
        name='oboe',
        short_name='ob.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[Bb3, A6]',
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

            >>> abjad.f(staff)
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

    known_percussion = list(sorted(set([
        'agogô',
        'anvil',
        'bass drum',
        'bongo drums',
        'cabasa',
        'cajón',
        'castanets',
        'caxixi',
        'claves',
        'conga drums',
        'cowbell',
        'crotales',
        'cuíca',
        'djembe',
        'finger cymbals',
        'flexatone',
        'frame drum',
        'gong',
        'güiro',
        'hand-held stones',
        'jawbone',
        'maracas',
        'ratchet',
        'rattle',
        'sand blocks',
        'scraped slate',
        'siren',
        'slapstick',
        'slide whistle',
        'snare drum',
        'sponges',
        'suspended cymbal',
        'steel drums',
        'tam-tam',
        'tambourine',
        'temple blocks',
        'thunder machine',
        'thundersheet',
        'toms',
        'tubular bells',
        'triangle',
        'vibraslap',
        'whistle',
        'wind chime',
        'wind machine',
        'wood blocks',
        'wood planks',
        ])))

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='percussion',
        short_name='perc.',
        markup=None,
        short_markup=None,
        allowable_clefs=('percussion',),
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

            >>> abjad.f(staff_group)
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
        name='piano',
        short_name='pf.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[A0, C8]',
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

            >>> abjad.f(staff)
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
        name='piccolo',
        short_name='picc.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='C5',
        pitch_range='[D5, C8]',
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

            >>> abjad.f(staff)
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
        name='sopranino saxophone',
        short_name='sopranino sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb4',
        pitch_range='[Db4, F#6]',
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

            >>> abjad.f(staff)
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
        name='soprano saxophone',
        short_name='sop. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb3',
        pitch_range='[Ab3, E6]',
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

            >>> abjad.f(staff)
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

    performer_abbreviation = 'sop.'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='soprano',
        short_name='sop.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C4, E6]',
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

            >>> abjad.f(staff)
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
        name='tenor saxophone',
        short_name='ten. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb2',
        pitch_range='[Ab2, E5]',
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

            >>> abjad.f(staff)
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
        name='tenor trombone',
        short_name='ten. trb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('tenor', 'bass'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[E2, Eb5]',
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

            >>> abjad.f(staff)
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

    performer_abbreviation = 'ten.'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='tenor',
        short_name='ten.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C3, D5]',
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

            >>> abjad.f(staff)
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
        name='trumpet',
        short_name='tp.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F#3, D6]',
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

            >>> abjad.f(staff)
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
        name='tuba',
        short_name='tb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[D1, F4]',
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

            >>> abjad.f(staff)
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
        name='vibraphone',
        short_name='vibr.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F3, F6]',
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

            >>> abjad.f(staff)
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

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='viola',
        short_name='va.',
        markup=None,
        short_markup=None,
        allowable_clefs=('alto', 'treble'),
        context=None,
        default_tuning=('C3', 'G3', 'D4', 'A4'),
        middle_c_sounding_pitch=None,
        pitch_range='[C3, D6]',
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
            Tuning(pitches=PitchSegment(['c', 'g', "d'", "a'"]))

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

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                fs'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='violin',
        short_name='vn.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        default_tuning=('G3', 'D4', 'A4', 'E5'),
        middle_c_sounding_pitch=None,
        pitch_range='[G3, G7]',
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
            Tuning(pitches=PitchSegment(['g', "d'", "a'", "e''"]))

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

            >>> abjad.f(staff)
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
        name='xylophone',
        short_name='xyl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='C5',
        pitch_range='[C4, C7]',
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
