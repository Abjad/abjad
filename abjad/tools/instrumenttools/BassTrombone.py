from abjad.tools.instrumenttools.Instrument import Instrument


class BassTrombone(Instrument):
    r'''Bass trombone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> bass_trombone = abjad.BassTrombone()
        >>> abjad.attach(bass_trombone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Bass trombone" }
                \set Staff.shortInstrumentName = \markup { "Bass trb." }
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
        name='bass trombone',
        short_name='bass trb.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[C2, F4]',
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

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass trombone's allowable clefs.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.allowable_clefs
            ('bass',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bass_trombone's written middle C.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(bass_trombone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bass trombone's name.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.name
            'bass trombone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets bass trombone's instrument name markup.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.name_markup
            Markup(contents=['Bass trombone'])

            >>> abjad.show(bass_trombone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass trombone's range.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.pitch_range
            PitchRange('[C2, F4]')

            >>> abjad.show(bass_trombone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets bass trombone's short instrument name.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.short_name
            'bass trb.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets bass trombone's short instrument name markup.

        ..  container:: example

            >>> bass_trombone = abjad.BassTrombone()
            >>> bass_trombone.short_name_markup
            Markup(contents=['Bass trb.'])

            >>> abjad.show(bass_trombone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
