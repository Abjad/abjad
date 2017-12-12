from abjad.tools.instrumenttools.Instrument import Instrument


class FrenchHorn(Instrument):
    r'''French horn.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> french_horn = abjad.FrenchHorn()
        >>> abjad.attach(french_horn, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Horn }
                \set Staff.shortInstrumentName = \markup { Hn. }
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
        name='horn',
        short_name='hn.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass', 'treble'),
        context=None,
        middle_c_sounding_pitch='F3',
        pitch_range='[B1, F5]',
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

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets French horn's allowable clefs.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.allowable_clefs
            ('bass', 'treble')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of French horn's written middle C.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.middle_c_sounding_pitch
            NamedPitch('f')

            >>> abjad.show(french_horn.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets French horn's name.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.name
            'horn'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets French horn's instrument name markup.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.name_markup
            Markup(contents=['Horn'])

            >>> abjad.show(french_horn.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets French horn's range.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.pitch_range
            PitchRange('[B1, F5]')

            >>> abjad.show(french_horn.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets French horn's short instrument name.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.short_name
            'hn.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets French horn's short instrument name markup.

        ..  container:: example

            >>> french_horn = abjad.FrenchHorn()
            >>> french_horn.short_name_markup
            Markup(contents=['Hn.'])

            >>> abjad.show(french_horn.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
