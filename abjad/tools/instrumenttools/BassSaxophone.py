from abjad.tools.instrumenttools.Instrument import Instrument


class BassSaxophone(Instrument):
    r'''Bass saxophone.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> bass_saxophone = abjad.instrumenttools.BassSaxophone()
            >>> abjad.attach(bass_saxophone, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Bass saxophone" }
                \set Staff.shortInstrumentName = \markup { "Bass sax." }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        name='bass saxophone',
        short_name='bass sax.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        middle_c_sounding_pitch='Bb1',
        pitch_range='[Ab2, E4]',
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
            'saxophonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass saxophone's allowable clefs.

        ..  container:: example

            ::

                >>> bass_saxophone.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(bass_saxophone.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bass_saxophone's written middle C.

        ..  container:: example

            ::

                >>> bass_saxophone.middle_c_sounding_pitch
                NamedPitch('bf,,')

            ::

                >>> show(bass_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bass saxophone's name.

        ..  container:: example

            ::

                >>> bass_saxophone.name
                'bass saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets bass saxophone's instrument name markup.

        ..  container:: example

            ::

                >>> bass_saxophone.name_markup
                Markup(contents=['Bass saxophone'])

            ::

                >>> show(bass_saxophone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass saxophone's range.

        ..  container:: example

            ::

                >>> bass_saxophone.pitch_range
                PitchRange('[Ab2, E4]')

            ::

                >>> show(bass_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets bass saxophone's short instrument name.

        ..  container:: example

            ::

                >>> bass_saxophone.short_name
                'bass sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets bass saxophone's short instrument name markup.

        ..  container:: example

            ::

                >>> bass_saxophone.short_name_markup
                Markup(contents=['Bass sax.'])

            ::

                >>> show(bass_saxophone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
