from abjad.tools.instrumenttools.Instrument import Instrument


class Marimba(Instrument):
    r'''Marimba.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> marimba = abjad.Marimba()
        >>> abjad.attach(marimba, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Marimba }
                \set Staff.shortInstrumentName = \markup { Mb. }
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
        name='marimba',
        short_name='mb.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F2, C7]',
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
        r'''Gets marimba's allowable clefs.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.allowable_clefs
            ('treble', 'bass')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of marimba's written middle C.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(marimba.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets marimba's name.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.name
            'marimba'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets marimba's instrument name markup.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.name_markup
            Markup(contents=['Marimba'])

            >>> abjad.show(marimba.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets marimba's range.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.pitch_range
            PitchRange('[F2, C7]')

            >>> abjad.show(marimba.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets marimba's short instrument name.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.short_name
            'mb.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets marimba's short instrument name markup.

        ..  container:: example

            >>> marimba = abjad.Marimba()
            >>> marimba.short_name_markup
            Markup(contents=['Mb.'])

            >>> abjad.show(marimba.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
