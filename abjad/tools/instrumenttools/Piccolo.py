from .Instrument import Instrument


class Piccolo(Instrument):
    r'''Piccolo.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> piccolo = abjad.Piccolo()
        >>> abjad.attach(piccolo, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Piccolo }
                \set Staff.shortInstrumentName = \markup { Picc. }
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
        name='piccolo',
        short_name='picc.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='C5',
        pitch_range='[D5, C8]',
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
        r'''Gets piccolo's allowable clefs.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets piccolo's instrument name markup.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.markup
            Markup(contents=['Piccolo'])

            >>> abjad.show(piccolo.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of piccolo's written middle C.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.middle_c_sounding_pitch
            NamedPitch("c''")

            >>> abjad.show(piccolo.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets piccolo's name.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.name
            'piccolo'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets piccolo's range.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.pitch_range
            PitchRange('[D5, C8]')

            >>> abjad.show(piccolo.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets piccolo's short instrument name markup.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.short_markup
            Markup(contents=['Picc.'])

            >>> abjad.show(piccolo.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets piccolo's short instrument name.

        ..  container:: example

            >>> piccolo = abjad.Piccolo()
            >>> piccolo.short_name
            'picc.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
