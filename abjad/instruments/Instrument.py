import copy
from abjad.system.AbjadValueObject import AbjadValueObject


class Instrument(AbjadValueObject):
    r"""
    Instrument.

    ..  container:: example

        Two instruments active on a single staff:

        >>> voice_1 = abjad.Voice("e'8 g'8 f'8 a'8")
        >>> flute = abjad.Flute(hide=True)
        >>> abjad.attach(flute, voice_1[0], context='Voice')
        >>> flute_markup = abjad.Markup('(flute)', direction=abjad.Up)
        >>> abjad.attach(flute_markup, voice_1[0])
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
        >>> voice_2 = abjad.Voice("c'2")
        >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
        >>> viola = abjad.Viola(hide=True)
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
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Instrument)
        ...
        (Note("e'8"), Flute(hide=True))
        (Note("g'8"), Flute(hide=True))
        (Note("f'8"), Flute(hide=True))
        (Note("a'8"), Flute(hide=True))

        >>> for leaf in abjad.select(voice_2).leaves():
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Instrument)
        ...
        (Note("c'2"), Viola(hide=True))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allowable_clefs',
        '_context',
        '_hide',
        '_middle_c_sounding_pitch',
        '_name',
        '_name_markup',
        '_is_primary_instrument',
        '_middle_c_sounding_pitch',
        '_performer_names',
        '_pitch_range',
        '_short_name',
        '_short_name_markup',
        '_starting_clefs',
        )

    _format_slot = 'opening'

    _latent = True

    _persistent = 'abjad.Instrument'

    _publish_storage_format = True

    _redraw = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allowable_clefs=None,
        context=None,
        hide=None,
        markup=None,
        middle_c_sounding_pitch=None,
        name=None,
        pitch_range=None,
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
        self._is_primary_instrument = False
        self._performer_names = ['instrumentalist']
        self._starting_clefs = copy.copy(allowable_clefs)
        if hide is not None:
            hide = bool(hide)
        self._hide = hide

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
        if self.hide is True:
            keywords.append('hide')
        return abjad.FormatSpecification(
            self,
            repr_args_values=[],
            repr_is_indented=False,
            repr_kwargs_names=keywords,
            )

    def _get_lilypond_format(self, context=None):
        import abjad
        result = []
        if self.hide:
            return result
        markup = self.markup
        if markup.direction is not None:
            markup = abjad.new(
                markup,
                direction=None,
                )
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._lilypond_type
        pieces = markup._get_format_pieces()
        first_line = r'\set {!s}.instrumentName = {!s}'
        first_line = first_line.format(context, pieces[0])
        result.append(first_line)
        result.extend(pieces[1:])
        short_markup = self.short_markup
        if short_markup.direction is not None:
            short_markup = abjad.new(
                short_markup,
                direction=None,
                )
        pieces = short_markup._get_format_pieces()
        first_line = r'\set {!s}.shortInstrumentName = {!s}'
        first_line = first_line.format(context, pieces[0])
        result.append(first_line)
        result.extend(pieces[1:])
        return result

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
    def hide(self):
        """
        Is true when instrument should not appear in output (but should
        still determine effective instrument).

        Use when instrument stays constant while margin markup changes.

        Defaults to none.

        Returns true, false or none.
        """
        return self._hide

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
    def persistent(self):
        """
        Is set to ``'abjad.Instrument'`` for all instruments.

        Class constant.

        Returns true.
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
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
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
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                    <d' fs' a'>4
                    e'4
                    r4
                    fs'4
                }

        Returns none.
        """
        import abjad
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
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
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
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
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                    <bf d' f'>4
                    c'4
                    r4
                    d'4
                }

        Returns none.
        """
        import abjad
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
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
