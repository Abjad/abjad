from abjad.tools.instrumenttools.Instrument import Instrument


class AltoTrombone(Instrument):
    r'''Alto trombone.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c4 d4 e4 fs4")
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[0])
            >>> alto_trombone = abjad.instrumenttools.AltoTrombone()
            >>> abjad.attach(alto_trombone, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Alto trombone" }
                \set Staff.shortInstrumentName = \markup { "Alt. trb." }
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
        name='alto trombone',
        short_name='alt. trb.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass', 'tenor'),
        middle_c_sounding_pitch=None,
        pitch_range='[A2, Bb5]',
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
            'brass player',
            'trombonist',
            ])
        self._starting_clefs = type(self.allowable_clefs)(['bass'])

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto trombone.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> alto_trombone = abjad.instrumenttools.AltoTrombone()
                >>> f(alto_trombone)
                instrumenttools.AltoTrombone(
                    name='alto trombone',
                    short_name='alt. trb.',
                    name_markup=abjad.Markup(
                        contents=['Alto trombone'],
                        ),
                    short_name_markup=abjad.Markup(
                        contents=['Alt. trb.'],
                        ),
                    allowable_clefs=instrumenttools.ClefList(
                        [
                            abjad.Clef(
                                name='bass',
                                ),
                            abjad.Clef(
                                name='tenor',
                                ),
                            ]
                        ),
                    middle_c_sounding_pitch=abjad.NamedPitch("c'"),
                    pitch_range=abjad.PitchRange('[A2, Bb5]'),
                    )

        Returns string.
        '''
        superclass = super(AltoTrombone, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto trombone's allowable clefs.

        ..  container:: example

            ::

                >>> alto_trombone.allowable_clefs
                ClefList([Clef(name='bass'), Clef(name='tenor')])

            ::

                >>> show(alto_trombone.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of alto trombone's written middle C.

        ..  container:: example

            ::

                >>> alto_trombone.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(alto_trombone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets alto trombone's name.

        ..  container:: example

            ::

                >>> alto_trombone.name
                'alto trombone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets alto trombone's instrument name markup.

        ..  container:: example

            ::

                >>> alto_trombone.name_markup
                Markup(contents=['Alto trombone'])

            ::

                >>> show(alto_trombone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto trombone's range.

        ..  container:: example

            ::

                >>> alto_trombone.pitch_range
                PitchRange('[A2, Bb5]')

            ::

                >>> show(alto_trombone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets alto trombone's short instrument name.

        ..  container:: example

            ::

                >>> alto_trombone.short_name
                'alt. trb.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets alto trombone's short instrument name markup.

        ..  container:: example

            ::

                >>> alto_trombone.short_name_markup
                Markup(contents=['Alt. trb.'])

            ::

                >>> show(alto_trombone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
