from .Instrument import Instrument


class Trumpet(Instrument):
    r'''Trumpet.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> trumpet = abjad.Trumpet()
        >>> abjad.attach(trumpet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { Trumpet }
                \set Staff.shortInstrumentName = \markup { Tp. }
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
        *,
        name='trumpet',
        short_name='tp.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F#3, D6]',
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
        r'''Gets trumpet's allowable clefs.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets trumpet's instrument name markup.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.markup
            Markup(contents=['Trumpet'])

            >>> abjad.show(trumpet.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of trumpet's written middle C.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(trumpet.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets trumpet's name.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.name
            'trumpet'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets trumpet's range.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.pitch_range
            PitchRange('[F#3, D6]')

            >>> abjad.show(trumpet.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets trumpet's short instrument name markup.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.short_markup
            Markup(contents=['Tp.'])

            >>> abjad.show(trumpet.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets trumpet's short instrument name.

        ..  container:: example

            >>> trumpet = abjad.Trumpet()
            >>> trumpet.short_name
            'tp.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
