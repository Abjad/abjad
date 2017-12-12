from abjad.tools.instrumenttools.Instrument import Instrument


class TenorTrombone(Instrument):
    r'''Tenor trombone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> tenor_trombone = abjad.TenorTrombone()
        >>> abjad.attach(tenor_trombone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Tenor trombone" }
                \set Staff.shortInstrumentName = \markup { "Ten. trb." }
                \clef "bass"
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
        name='tenor trombone',
        short_name='ten. trb.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('tenor', 'bass'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[E2, Eb5]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            pitch_range=pitch_range,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tenor trombone's allowable clefs.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.allowable_clefs
            ('tenor', 'bass')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of tenor trombone's written middle C.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(tenor_trombone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets tenor trombone's name.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.name
            'tenor trombone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets tenor trombone's instrument name markup.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.name_markup
            Markup(contents=['Tenor trombone'])

            >>> abjad.show(tenor_trombone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tenor trombone's range.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.pitch_range
            PitchRange('[E2, Eb5]')

            >>> abjad.show(tenor_trombone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets tenor trombone's short instrument name.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.short_name
            'ten. trb.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets tenor trombone's short instrument name markup.

        ..  container:: example

            >>> tenor_trombone = abjad.TenorTrombone()
            >>> tenor_trombone.short_name_markup
            Markup(contents=['Ten. trb.'])

            >>> abjad.show(tenor_trombone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
