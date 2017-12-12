from abjad.tools.instrumenttools.Instrument import Instrument


class ClarinetInBFlat(Instrument):
    r'''Clarinet in B-flat.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = abjad.ClarinetInBFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'cl.'

    ### INITIALIZER ###

    def __init__(
        self,
        name='clarinet in B-flat',
        short_name='cl. in B-flat',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb3',
        pitch_range='[D3, Bb6]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets clarinet in B-flat's allowable clefs.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of clarinet in B-flat's written middle C.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.middle_c_sounding_pitch
            NamedPitch('bf')

            >>> abjad.show(clarinet.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets clarinet in B-flat's name.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.name
            'clarinet in B-flat'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets clarinet in B-flat's instrument name markup.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.name_markup
            Markup(contents=['Clarinet in B-flat'])

            >>> abjad.show(clarinet.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets clarinet in B-flat's range.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.pitch_range
            PitchRange('[D3, Bb6]')

            >>> abjad.show(clarinet.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets clarinet in B-flat's short instrument name.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.short_name
            'cl. in B-flat'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets clarinet in B-flat's short instrument name markup.

        ..  container:: example

            >>> clarinet = abjad.ClarinetInBFlat()
            >>> clarinet.short_name_markup
            Markup(contents=['Cl. in B-flat'])

            >>> abjad.show(clarinet.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
