from abjad.tools.instrumenttools.Instrument import Instrument


class TenorVoice(Instrument):
    r'''Tenor voice.

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> tenor = abjad.instrumenttools.TenorVoice()
            >>> abjad.attach(tenor, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Tenor }
                \set Staff.shortInstrumentName = \markup { Ten. }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'ten.'

    ### INITIALIZER ###

    def __init__(
        self,
        name='tenor',
        short_name='ten.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C3, D5]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._performer_names.extend([
            'vocalist',
            'tenor',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tenor's allowable clefs.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(tenor.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of tenor's written middle C.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(tenor.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets tenor's name.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.name
                'tenor'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets tenor's instrument name markup.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.name_markup
                Markup(contents=['Tenor'])

            ::

                >>> show(tenor.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tenor's range.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.pitch_range
                PitchRange('[C3, D5]')

            ::

                >>> show(tenor.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets tenor's short instrument name.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.short_name
                'ten.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets tenor's short instrument name markup.

        ..  container:: example

            ::

                >>> tenor = abjad.instrumenttools.TenorVoice()
                >>> tenor.short_name_markup
                Markup(contents=['Ten.'])

            ::

                >>> show(tenor.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
