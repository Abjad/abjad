from .Instrument import Instrument


class ContrabassSaxophone(Instrument):
    r'''Contrabass saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_saxophone = abjad.ContrabassSaxophone()
        >>> abjad.attach(contrabass_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { "Contrabass saxophone" }
                \set Staff.shortInstrumentName = \markup { "Cbass. sax." }
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
        name='contrabass saxophone',
        short_name='cbass. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb1',
        pitch_range='[C1, Ab3]',
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
        r'''Gets contrabass saxophone's allowable clefs.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets contrabass saxophone's instrument name markup.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.markup
            Markup(contents=['Contrabass saxophone'])

            >>> abjad.show(contrabass_saxophone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of contrabass_saxophone's written middle C.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.middle_c_sounding_pitch
            NamedPitch('ef,,')

            >>> abjad.show(contrabass_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets contrabass saxophone's name.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.name
            'contrabass saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabass saxophone's range.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.pitch_range
            PitchRange('[C1, Ab3]')

            >>> abjad.show(contrabass_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets contrabass saxophone's short instrument name markup.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.short_markup
            Markup(contents=['Cbass. sax.'])

            >>> abjad.show(contrabass_saxophone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets contrabass saxophone's short instrument name.

        ..  container:: example

            >>> contrabass_saxophone = abjad.ContrabassSaxophone()
            >>> contrabass_saxophone.short_name
            'cbass. sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
