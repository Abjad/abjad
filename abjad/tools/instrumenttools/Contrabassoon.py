# -*- coding: utf-8 -*-
from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabassoon(Instrument):
    r'''A contrabassoon.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> contrabassoon = instrumenttools.Contrabassoon()
        >>> attach(contrabassoon, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Contrabassoon }
            \set Staff.shortInstrumentName = \markup { Contrabsn. }
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
        instrument_name='contrabassoon',
        short_instrument_name='contrabsn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass',),
        pitch_range='[Bb0, Bb4]',
        sounding_pitch_of_written_middle_c='C3',
        ):
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._performer_names.extend([
            'wind player',
            'reed player',
            'double reed player',
            'bassoonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets contrabassoon's allowable clefs.

        ..  container:: example

            ::

                >>> contrabassoon.allowable_clefs
                ClefInventory([Clef(name='bass')])

            ::

                >>> show(contrabassoon.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets contrabassoon's name.

        ..  container:: example

            ::

                >>> contrabassoon.instrument_name
                'contrabassoon'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets contrabassoon's instrument name markup.

        ..  container:: example

            ::

                >>> contrabassoon.instrument_name_markup
                Markup(contents=('Contrabassoon',))

            ::

                >>> show(contrabassoon.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabassoon's range.

        ..  container:: example

            ::

                >>> contrabassoon.pitch_range
                PitchRange(range_string='[Bb0, Bb4]')

            ::

                >>> show(contrabassoon.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets contrabassoon's short instrument name.

        ..  container:: example

            ::

                >>> contrabassoon.short_instrument_name
                'contrabsn.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets contrabassoon's short instrument name markup.

        ..  container:: example

            ::

                >>> contrabassoon.short_instrument_name_markup
                Markup(contents=('Contrabsn.',))

            ::

                >>> show(contrabassoon.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of contrabassoon's written middle C.

        ..  container:: example

            ::

                >>> contrabassoon.sounding_pitch_of_written_middle_c
                NamedPitch('c')

            ::

                >>> show(contrabassoon.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
