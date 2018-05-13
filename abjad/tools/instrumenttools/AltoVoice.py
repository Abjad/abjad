from .Instrument import Instrument


class AltoVoice(Instrument):
    r'''Alto voice.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> alto = abjad.AltoVoice()
        >>> abjad.attach(alto, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { Alto }
                \set Staff.shortInstrumentName = \markup { Alto }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

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
        r'''Gets alto's allowable clefs.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets alto's instrument name markup.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.markup
            Markup(contents=['Alto'])

            >>> abjad.show(alto.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of alto's written middle C.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(alto.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets alto's name.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.name
            'alto'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto's range.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.pitch_range
            PitchRange('[F3, G5]')

            >>> abjad.show(alto.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets alto's short instrument name markup.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.short_markup
            Markup(contents=['Alto'])

            >>> abjad.show(alto.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets alto's short instrument name.

        ..  container:: example

            >>> alto = abjad.AltoVoice()
            >>> alto.short_name
            'alto'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
