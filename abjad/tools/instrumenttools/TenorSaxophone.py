from .Instrument import Instrument


class TenorSaxophone(Instrument):
    r'''Tenor saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> tenor_saxophone = abjad.TenorSaxophone()
        >>> abjad.attach(tenor_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { "Tenor saxophone" }
                \set Staff.shortInstrumentName = \markup { "Ten. sax." }
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
        name='tenor saxophone',
        short_name='ten. sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb2',
        pitch_range='[Ab2, E5]',
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
        r'''Gets tenor saxophone's allowable clefs.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets tenor saxophone's instrument name markup.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.markup
            Markup(contents=['Tenor saxophone'])

            >>> abjad.show(tenor_saxophone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of tenor saxophone's written middle C.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.middle_c_sounding_pitch
            NamedPitch('bf,')

            >>> abjad.show(tenor_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets tenor saxophone's name.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.name
            'tenor saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tenor saxophone's range.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.pitch_range
            PitchRange('[Ab2, E5]')

            >>> abjad.show(tenor_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets tenor saxophone's short instrument name markup.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.short_markup
            Markup(contents=['Ten. sax.'])

            >>> abjad.show(tenor_saxophone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets tenor saxophone's short instrument name.

        ..  container:: example

            >>> tenor_saxophone = abjad.TenorSaxophone()
            >>> tenor_saxophone.short_name
            'ten. sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
