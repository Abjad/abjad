from .Instrument import Instrument


class Glockenspiel(Instrument):
    r'''Glockenspiel.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> glockenspiel = abjad.Glockenspiel()
        >>> abjad.attach(glockenspiel, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Glockenspiel }
                \set Staff.shortInstrumentName = \markup { Gkspl. }
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
        name='glockenspiel',
        short_name='gkspl.',
        markup=None,
        short_markup=None,
        allowable_clefs=None,
        context=None,
        middle_c_sounding_pitch='C6',
        pitch_range='[G5, C8]',
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
        r'''Gets glockenspiel's allowable clefs.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets glockenspiel's instrument name markup.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.markup
            Markup(contents=['Glockenspiel'])

            >>> abjad.show(glockenspiel.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r"""Gets sounding pitch of glockenspiel's written middle C.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.middle_c_sounding_pitch
            NamedPitch("c'''")

            >>> abjad.show(glockenspiel.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        """
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets glockenspiel's name.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.name
            'glockenspiel'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets glockenspiel's range.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.pitch_range
            PitchRange('[G5, C8]')

            >>> abjad.show(glockenspiel.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets glockenspiel's short instrument name markup.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.short_markup
            Markup(contents=['Gkspl.'])

            >>> abjad.show(glockenspiel.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets glockenspiel's short instrument name.

        ..  container:: example

            >>> glockenspiel = abjad.Glockenspiel()
            >>> glockenspiel.short_name
            'gkspl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
