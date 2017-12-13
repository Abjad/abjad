from .Instrument import Instrument


class Tuba(Instrument):
    r'''Tuba.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> tuba = abjad.Tuba()
        >>> abjad.attach(tuba, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Tuba }
                \set Staff.shortInstrumentName = \markup { Tb. }
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
        name='tuba',
        short_name='tb.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[D1, F4]',
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
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tuba's allowable clefs.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.allowable_clefs
            ('bass',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets tuba's instrument name markup.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.markup
            Markup(contents=['Tuba'])

            >>> abjad.show(tuba.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of tuba's written middle C.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(tuba.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets tuba's name.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.name
            'tuba'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tuba's range.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.pitch_range
            PitchRange('[D1, F4]')

            >>> abjad.show(tuba.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets tuba's short instrument name markup.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.short_markup
            Markup(contents=['Tb.'])

            >>> abjad.show(tuba.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets tuba's short instrument name.

        ..  container:: example

            >>> tuba = abjad.Tuba()
            >>> tuba.short_name
            'tb.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
