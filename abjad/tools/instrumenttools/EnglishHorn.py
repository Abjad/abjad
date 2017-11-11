from abjad.tools.instrumenttools.Instrument import Instrument


class EnglishHorn(Instrument):
    r'''English horn.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> english_horn = abjad.EnglishHorn()
        >>> abjad.attach(english_horn, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "English horn" }
                \set Staff.shortInstrumentName = \markup { "Eng. hn." }
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
        name='English horn',
        short_name='Eng. hn.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='F3',
        pitch_range='[E3, C6]',
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
        r'''Gets English horn's allowable clefs.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of English horn's written middle C.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.middle_c_sounding_pitch
            NamedPitch('f')

            >>> abjad.show(english_horn.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets English horn's name.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.name
            'English horn'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets English horn's instrument name markup.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.name_markup
            Markup(contents=['English horn'])

            >>> abjad.show(english_horn.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets English horn's range.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.pitch_range
            PitchRange('[E3, C6]')

            >>> abjad.show(english_horn.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets English horn's short instrument name.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.short_name
            'Eng. hn.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets English horn's short instrument name markup.

        ..  container:: example

            >>> english_horn = abjad.EnglishHorn()
            >>> english_horn.short_name_markup
            Markup(contents=['Eng. hn.'])

            >>> abjad.show(english_horn.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
