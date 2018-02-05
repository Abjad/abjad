from .Instrument import Instrument


class Vibraphone(Instrument):
    r'''Vibraphone.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> vibraphone = abjad.Vibraphone()
        >>> abjad.attach(vibraphone, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { Vibraphone }
                \set Staff.shortInstrumentName = \markup { Vibr. }
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
        name='vibraphone',
        short_name='vibr.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[F3, F6]',
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
        r'''Gets vibraphone's allowable clefs.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets vibraphone's instrument name markup.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.markup
            Markup(contents=['Vibraphone'])

            >>> abjad.show(vibraphone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of vibraphone's written middle C.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(vibraphone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets vibraphone's name.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.name
            'vibraphone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets vibraphone's range.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.pitch_range
            PitchRange('[F3, F6]')

            >>> abjad.show(vibraphone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets vibraphone's short instrument name markup.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.short_markup
            Markup(contents=['Vibr.'])

            >>> abjad.show(vibraphone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets vibraphone's short instrument name.

        ..  container:: example

            >>> vibraphone = abjad.Vibraphone()
            >>> vibraphone.short_name
            'vibr.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
