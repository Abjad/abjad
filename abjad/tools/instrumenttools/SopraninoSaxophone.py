from .Instrument import Instrument


class SopraninoSaxophone(Instrument):
    r'''Sopranino saxophone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> sopranino_saxophone = abjad.SopraninoSaxophone()
        >>> abjad.attach(sopranino_saxophone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { "Sopranino saxophone" }
                \set Staff.shortInstrumentName = \markup { "Sopranino sax." }
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
        name='sopranino saxophone',
        short_name='sopranino sax.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='Eb4',
        pitch_range='[Db4, F#6]',
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
        r'''Gets sopranino saxophone's allowable clefs.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets sopranino saxophone's instrument name markup.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.markup
            Markup(contents=['Sopranino saxophone'])

            >>> abjad.show(sopranino_saxophone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of sopranino saxophone's written middle C.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.middle_c_sounding_pitch
            NamedPitch("ef'")

            >>> abjad.show(sopranino_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets sopranino saxophone's name.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.name
            'sopranino saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets sopranino saxophone's range.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.pitch_range
            PitchRange('[Db4, F#6]')

            >>> abjad.show(sopranino_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets sopranino saxophone's short instrument name markup.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.short_markup
            Markup(contents=['Sopranino sax.'])

            >>> abjad.show(sopranino_saxophone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets sopranino saxophone's short instrument name.

        ..  container:: example

            >>> sopranino_saxophone = abjad.SopraninoSaxophone()
            >>> sopranino_saxophone.short_name
            'sopranino sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
