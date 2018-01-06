from .Instrument import Instrument


class Guitar(Instrument):
    r'''Guitar.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> guitar = abjad.Guitar()
        >>> abjad.attach(guitar, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Guitar }
                \set Staff.shortInstrumentName = \markup { Gt. }
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
        name='guitar',
        short_name='gt.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        default_tuning=('E2', 'A2', 'D3', 'G3', 'B3', 'E4'),
        middle_c_sounding_pitch='C3',
        pitch_range='[E2, E5]',
        hide=None,
        ):
        import abjad
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
        self._is_primary_instrument = True
        self._default_tuning = abjad.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets guitar's allowable clefs.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets guitar's default tuning.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.default_tuning
            Tuning(pitches=PitchSegment(['e,', 'a,', 'd', 'g', 'b', "e'"]))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def markup(self):
        r'''Gets guitar's instrument name markup.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.markup
            Markup(contents=['Guitar'])

            >>> abjad.show(guitar.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of guitar's written middle C.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.middle_c_sounding_pitch
            NamedPitch('c')

            >>> abjad.show(guitar.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets guitar's name.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.name
            'guitar'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets guitar's range.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.pitch_range
            PitchRange('[E2, E5]')

            >>> abjad.show(guitar.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets guitar's short instrument name markup.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.short_markup
            Markup(contents=['Gt.'])

            >>> abjad.show(guitar.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets guitar's short instrument name.

        ..  container:: example

            >>> guitar = abjad.Guitar()
            >>> guitar.short_name
            'gt.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
