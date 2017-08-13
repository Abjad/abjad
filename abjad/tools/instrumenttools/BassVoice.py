from abjad.tools.instrumenttools.Instrument import Instrument


class BassVoice(Instrument):
    r'''Bass voice.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c4 d4 e4 fs4")
            >>> bass = abjad.instrumenttools.BassVoice()
            >>> abjad.attach(bass, staff[0])
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Bass }
                \set Staff.shortInstrumentName = \markup { Bass }
                \clef "bass"
                c4
                d4
                e4
                fs4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        name='bass',
        short_name='bass',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass',),
        middle_c_sounding_pitch=None,
        pitch_range='[E2, F4]',
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
            'bass',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass's allowable clefs.

        ..  container:: example

            ::

                >>> bass.allowable_clefs
                ClefList([Clef(name='bass')])

            ::

                >>> show(bass.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bass's written middle C.

        ..  container:: example

            ::

                >>> bass.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(bass.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bass's name.

        ..  container:: example

            ::

                >>> bass.name
                'bass'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets bass's instrument name markup.

        ..  container:: example

            ::

                >>> bass.name_markup
                Markup(contents=['Bass'])

            ::

                >>> show(bass.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass's range.

        ..  container:: example

            ::

                >>> bass.pitch_range
                PitchRange('[E2, F4]')

            ::

                >>> show(bass.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets bass's short instrument name.

        ..  container:: example

            ::

                >>> bass.short_name
                'bass'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets bass's short instrument name markup.

        ..  container:: example

            ::

                >>> bass.short_name_markup
                Markup(contents=['Bass'])

            ::

                >>> show(bass.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
