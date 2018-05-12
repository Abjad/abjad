from .Instrument import Instrument


class BassSaxophone(Instrument):
    r'''Bass saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> bass_saxophone = abjad.BassSaxophone()
        >>> abjad.attach(bass_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
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
        *,
        name='bass saxophone',
        short_name='bass sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Bb1',
        pitch_range='[Ab2, E4]',
        hide=None,
        ):
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

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass saxophone's allowable clefs.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets bass saxophone's instrument name markup.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.markup
            Markup(contents=['Bass saxophone'])

            >>> abjad.show(bass_saxophone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bass_saxophone's written middle C.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.middle_c_sounding_pitch
            NamedPitch('bf,,')

            >>> abjad.show(bass_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bass saxophone's name.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.name
            'bass saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass saxophone's range.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.pitch_range
            PitchRange('[Ab2, E4]')

            >>> abjad.show(bass_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets bass saxophone's short instrument name markup.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.short_markup
            Markup(contents=['Bass sax.'])

            >>> abjad.show(bass_saxophone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets bass saxophone's short instrument name.

        ..  container:: example

            >>> bass_saxophone = abjad.BassSaxophone()
            >>> bass_saxophone.short_name
            'bass sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
