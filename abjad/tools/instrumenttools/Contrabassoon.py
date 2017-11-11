from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabassoon(Instrument):
    r'''Contrabassoon.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> contrabassoon = abjad.Contrabassoon()
        >>> abjad.attach(contrabassoon, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Contrabassoon }
                \set Staff.shortInstrumentName = \markup { Contrabsn. }
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
        name='contrabassoon',
        short_name='contrabsn.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch='C3',
        pitch_range='[Bb0, Bb4]',
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
        r'''Gets contrabassoon's allowable clefs.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.allowable_clefs
            ('bass',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of contrabassoon's written middle C.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.middle_c_sounding_pitch
            NamedPitch('c')

            >>> abjad.show(contrabassoon.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets contrabassoon's name.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.name
            'contrabassoon'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets contrabassoon's instrument name markup.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.name_markup
            Markup(contents=['Contrabassoon'])

            >>> abjad.show(contrabassoon.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabassoon's range.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.pitch_range
            PitchRange('[Bb0, Bb4]')

            >>> abjad.show(contrabassoon.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets contrabassoon's short instrument name.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.short_name
            'contrabsn.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets contrabassoon's short instrument name markup.

        ..  container:: example

            >>> contrabassoon = abjad.Contrabassoon()
            >>> contrabassoon.short_name_markup
            Markup(contents=['Contrabsn.'])

            >>> abjad.show(contrabassoon.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
