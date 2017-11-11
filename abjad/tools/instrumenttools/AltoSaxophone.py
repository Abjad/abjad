from abjad.tools.instrumenttools.Instrument import Instrument


class AltoSaxophone(Instrument):
    r'''Alto saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> alto_saxophone = abjad.AltoSaxophone()
        >>> abjad.attach(alto_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Alto saxophone" }
                \set Staff.shortInstrumentName = \markup { "Alt. sax." }
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
        name='alto saxophone',
        short_name='alt. sax.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb3',
        pitch_range='[Db3, A5]',
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

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto sax.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            >>> alto_sax = abjad.AltoSaxophone()
            >>> abjad.f(alto_sax)
            abjad.AltoSaxophone(
                name='alto saxophone',
                short_name='alt. sax.',
                name_markup=abjad.Markup(
                    contents=['Alto saxophone'],
                    ),
                short_name_markup=abjad.Markup(
                    contents=['Alt. sax.'],
                    ),
                allowable_clefs=('treble',),
                context='Staff',
                middle_c_sounding_pitch=abjad.NamedPitch('ef'),
                pitch_range=abjad.PitchRange('[Db3, A5]'),
                )

        Returns string.
        '''
        superclass = super(AltoSaxophone, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto saxophone's allowable clefs.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of alto saxophone's written middle C.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.middle_c_sounding_pitch
            NamedPitch('ef')

            >>> abjad.show(alto_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets alto saxophone's name.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.name
            'alto saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets alto saxophone's instrument name markup.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.name_markup
            Markup(contents=['Alto saxophone'])

            >>> abjad.show(alto_saxophone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto saxophone's range.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.pitch_range
            PitchRange('[Db3, A5]')

            >>> abjad.show(alto_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets alto saxophone's short instrument name.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.short_name
            'alt. sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets alto saxophone's short instrument name markup.

        ..  container:: example

            >>> alto_saxophone = abjad.AltoSaxophone()
            >>> alto_saxophone.short_name_markup
            Markup(contents=['Alt. sax.'])

            >>> abjad.show(alto_saxophone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
