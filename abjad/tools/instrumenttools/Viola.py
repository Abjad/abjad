from abjad.tools.instrumenttools.Instrument import Instrument


class Viola(Instrument):
    r'''Viola.

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> clef = abjad.Clef('alto')
            >>> abjad.attach(clef, staff[0])
            >>> viola = abjad.instrumenttools.Viola()
            >>> abjad.attach(viola, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Viola }
                \set Staff.shortInstrumentName = \markup { Va. }
                \clef "alto"
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name='viola',
        short_name='va.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('alto', 'treble'),
        default_tuning=('C3', 'G3', 'D4', 'A4'),
        middle_c_sounding_pitch=None,
        pitch_range='[C3, D6]',
        ):
        import abjad
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            )
        self._performer_names.extend([
            'string player',
            'violist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = type(self.allowable_clefs)(['alto'])
        self._default_tuning = abjad.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets viola's allowable clefs.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.allowable_clefs
                ClefList([Clef('alto'), Clef('treble')])

            ::

                >>> show(viola.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets viola's default tuning.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.default_tuning
                Tuning(pitches=PitchSegment(['c', 'g', "d'", "a'"]))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of viola's written middle C.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(viola.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets viola's name.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.name
                'viola'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets viola's instrument name markup.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.name_markup
                Markup(contents=['Viola'])

            ::

                >>> show(viola.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets viola's range.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.pitch_range
                PitchRange('[C3, D6]')

            ::

                >>> show(viola.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets viola's short instrument name.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.short_name
                'va.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets viola's short instrument name markup.

        ..  container:: example

            ::

                >>> viola = abjad.instrumenttools.Viola()
                >>> viola.short_name_markup
                Markup(contents=['Va.'])

            ::

                >>> show(viola.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
