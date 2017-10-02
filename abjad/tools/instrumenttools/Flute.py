from abjad.tools.instrumenttools.Instrument import Instrument


class Flute(Instrument):
    r'''Flute.

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> flute = abjad.Flute()
            >>> abjad.attach(flute, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Flute }
                \set Staff.shortInstrumentName = \markup { Fl. }
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
        name='flute',
        short_name='fl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        default_scope=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C4, D7]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            default_scope=default_scope,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets flute's allowable clefs.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.allowable_clefs
                ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of flute's written middle C.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(flute.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets flute's name.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.name
                'flute'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets flute's instrument name markup.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.name_markup
                Markup(contents=['Flute'])

            ::

                >>> show(flute.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets flute's range.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.pitch_range
                PitchRange('[C4, D7]')

            ::

                >>> show(flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets flute's short instrument name.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.short_name
                'fl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets flute's short instrument name markup.

        ..  container:: example

            ::

                >>> flute = abjad.Flute()
                >>> flute.short_name_markup
                Markup(contents=['Fl.'])

            ::

                >>> show(flute.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
