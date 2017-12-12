from abjad.tools.instrumenttools.Instrument import Instrument


class AltoFlute(Instrument):
    r'''Alto flute.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> alto_flute = abjad.AltoFlute()
        >>> abjad.attach(alto_flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Alto flute" }
                \set Staff.shortInstrumentName = \markup { "Alt. fl." }
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
        name='alto flute',
        short_name='alt. fl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='G3',
        pitch_range='[G3, G6]',
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

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto flute.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> abjad.f(alto_flute)
            abjad.AltoFlute(
                name='alto flute',
                short_name='alt. fl.',
                name_markup=abjad.Markup(
                    contents=['Alto flute'],
                    ),
                short_name_markup=abjad.Markup(
                    contents=['Alt. fl.'],
                    ),
                allowable_clefs=('treble',),
                context='Staff',
                middle_c_sounding_pitch=abjad.NamedPitch('g'),
                pitch_range=abjad.PitchRange('[G3, G6]'),
                )

        Returns string.
        '''
        superclass = super(AltoFlute, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto flute's allowable clefs.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of alto flute's written middle C.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.middle_c_sounding_pitch
            NamedPitch('g')

            >>> abjad.show(alto_flute.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets alto flute's name.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.name
            'alto flute'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets alto flute's instrument name markup.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.name_markup
            Markup(contents=['Alto flute'])

            >>> abjad.show(alto_flute.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto flute's range.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.pitch_range
            PitchRange('[G3, G6]')

            >>> abjad.show(alto_flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets alto flute's short instrument name.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.short_name
            'alt. fl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets alto flute's short instrument name markup.

        ..  container:: example

            >>> alto_flute = abjad.AltoFlute()
            >>> alto_flute.short_name_markup
            Markup(contents=['Alt. fl.'])

            >>> abjad.show(alto_flute.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
