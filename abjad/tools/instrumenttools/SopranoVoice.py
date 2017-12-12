from abjad.tools.instrumenttools.Instrument import Instrument


class SopranoVoice(Instrument):
    r'''Soprano voice.

    ..  container:: example

        >>> staff = abjad.Staff("c''4 d''4 e''4 fs''4")
        >>> soprano = abjad.SopranoVoice()
        >>> abjad.attach(soprano, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Soprano }
                \set Staff.shortInstrumentName = \markup { Sop. }
                c''4
                d''4
                e''4
                fs''4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'sop.'

    ### INITIALIZER ###

    def __init__(
        self,
        name='soprano',
        short_name='sop.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C4, E6]',
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
        r'''Gets soprano's allowable clefs.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of soprano's written middle C.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(soprano.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets soprano's name.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.name
            'soprano'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets soprano's instrument name markup.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.name_markup
            Markup(contents=['Soprano'])

            >>> abjad.show(soprano.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets soprano's range.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.pitch_range
            PitchRange('[C4, E6]')

            >>> abjad.show(soprano.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets soprano's short instrument name.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.short_name
            'sop.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets soprano's short instrument name markup.

        ..  container:: example

            >>> soprano = abjad.SopranoVoice()
            >>> soprano.short_name_markup
            Markup(contents=['Sop.'])

            >>> abjad.show(soprano.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
