from .Instrument import Instrument


class MezzoSopranoVoice(Instrument):
    r'''Mezzo-soprano voice.

    ..  container:: example


        >>> staff = abjad.Staff("c''4 d''4 e''4 fs''4")
        >>> mezzo_soprano = abjad.MezzoSopranoVoice()
        >>> abjad.attach(mezzo_soprano, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { Mezzo-soprano }
                \set Staff.shortInstrumentName = \markup { Mezz. }
                c''4
                d''4
                e''4
                fs''4
            }

    '''

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
            pitch_range=pitch_range,
            hide=hide,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets mezzo-soprano's allowable clefs.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets mezzo-soprano's instrument name markup.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.markup
            Markup(contents=['Mezzo-soprano'])

            >>> abjad.show(mezzo_soprano.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of mezzo-soprano's written middle C.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(mezzo_soprano.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets mezzo-soprano's name.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.name
            'mezzo-soprano'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets mezzo-soprano's range.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.pitch_range
            PitchRange('[A3, C6]')

            >>> abjad.show(mezzo_soprano.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets mezzo-soprano's short instrument name markup.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.short_markup
            Markup(contents=['Mezz.'])

            >>> abjad.show(mezzo_soprano.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets mezzo-soprano's short instrument name.

        ..  container:: example

            >>> mezzo_soprano = abjad.MezzoSopranoVoice()
            >>> mezzo_soprano.short_name
            'mezz.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
