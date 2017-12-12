from abjad.tools.instrumenttools.Instrument import Instrument


class ContrabassFlute(Instrument):
    r'''Contrabass flute.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_flute = abjad.ContrabassFlute()
        >>> abjad.attach(contrabass_flute, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Contrabass flute" }
                \set Staff.shortInstrumentName = \markup { "Cbass. fl." }
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
        name='contrabass flute',
        short_name='cbass. fl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='G2',
        pitch_range='[G2, G5]',
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
        r'''Gets contrabass flute's allowable clefs.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of contrabass_flute's written middle C.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.middle_c_sounding_pitch
            NamedPitch('g,')

            >>> abjad.show(contrabass_flute.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets contrabass flute's name.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.name
            'contrabass flute'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets contrabass flute's instrument name markup.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.name_markup
            Markup(contents=['Contrabass flute'])

            >>> abjad.show(contrabass_flute.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabass flute's range.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.pitch_range
            PitchRange('[G2, G5]')

            >>> abjad.show(contrabass_flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets contrabass flute's short instrument name.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.short_name
            'cbass. fl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets contrabass flute's short instrument name markup.

        ..  container:: example

            >>> contrabass_flute = abjad.ContrabassFlute()
            >>> contrabass_flute.short_name_markup
            Markup(contents=['Cbass. fl.'])

            >>> abjad.show(contrabass_flute.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
