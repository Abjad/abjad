from abjad.tools.instrumenttools.Instrument import Instrument


class Bassoon(Instrument):
    r'''Bassoon.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> bassoon = abjad.Bassoon()
        >>> abjad.attach(bassoon, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Bassoon }
                \set Staff.shortInstrumentName = \markup { Bsn. }
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
        name='bassoon',
        short_name='bsn.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass', 'tenor'),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[Bb1, Eb5]',
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
        r'''Gets bassoon's allowable clefs.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.allowable_clefs
            ('bass', 'tenor')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bassoon's written middle C.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(bassoon.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bassoon's name.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.name
            'bassoon'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets bassoon's instrument name markup.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.name_markup
            Markup(contents=['Bassoon'])

            >>> abjad.show(bassoon.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bassoon's range.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.pitch_range
            PitchRange('[Bb1, Eb5]')

            >>> abjad.show(bassoon.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets bassoon's short instrument name.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.short_name
            'bsn.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets bassoon's short instrument name markup.

        ..  container:: example

            >>> bassoon = abjad.Bassoon()
            >>> bassoon.short_name_markup
            Markup(contents=['Bsn.'])

            >>> abjad.show(bassoon.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
