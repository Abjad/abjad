from abjad.tools.instrumenttools.Instrument import Instrument


class BassClarinet(Instrument):
    r'''Bass clarinet.

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
            >>> abjad.attach(bass_clarinet, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Bass clarinet" }
                \set Staff.shortInstrumentName = \markup { "Bass cl." }
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
        name='bass clarinet',
        short_name='bass cl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        middle_c_sounding_pitch='Bb2',
        pitch_range='[Bb1, G5]',
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
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._starting_clefs = type(self.allowable_clefs)(['treble'])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass clarinet's allowable clefs.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.allowable_clefs
                ClefList([Clef('treble'), Clef('bass')])

            ::

                >>> show(bass_clarinet.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bass_clarinet's written middle C.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.middle_c_sounding_pitch
                NamedPitch('bf,')

            ::

                >>> show(bass_clarinet.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bass clarinet's name.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.name
                'bass clarinet'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets bass clarinet's instrument name markup.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.name_markup
                Markup(contents=['Bass clarinet'])

            ::

                >>> show(bass_clarinet.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass clarinet's range.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.pitch_range
                PitchRange('[Bb1, G5]')

            ::

                >>> show(bass_clarinet.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets bass clarinet's short instrument name.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.short_name
                'bass cl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets bass clarinet's short instrument name markup.

        ..  container:: example

            ::

                >>> bass_clarinet = abjad.instrumenttools.BassClarinet()
                >>> bass_clarinet.short_name_markup
                Markup(contents=['Bass cl.'])

            ::

                >>> show(bass_clarinet.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
