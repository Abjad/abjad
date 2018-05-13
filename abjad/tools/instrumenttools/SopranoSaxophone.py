from .Instrument import Instrument


class SopranoSaxophone(Instrument):
    r'''Soprano saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> soprano_saxophone = abjad.SopranoSaxophone()
        >>> abjad.attach(soprano_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { "Soprano saxophone" }
                \set Staff.shortInstrumentName = \markup { "Sop. sax." }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

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
        hide=None,
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
            hide=hide,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets soprano saxophone's allowable clefs.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets soprano saxophone's instrument name markup.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.markup
            Markup(contents=['Soprano saxophone'])

            >>> abjad.show(soprano_saxophone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of soprano saxophone's written middle C.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.middle_c_sounding_pitch
            NamedPitch('bf')

            >>> abjad.show(soprano_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets soprano saxophone's name.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.name
            'soprano saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets soprano saxophone's range.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.pitch_range
            PitchRange('[Ab3, E6]')

            >>> abjad.show(soprano_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets soprano saxophone's short instrument name markup.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.short_markup
            Markup(contents=['Sop. sax.'])

            >>> abjad.show(soprano_saxophone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets soprano saxophone's short instrument name.

        ..  container:: example

            >>> soprano_saxophone = abjad.SopranoSaxophone()
            >>> soprano_saxophone.short_name
            'sop. sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
