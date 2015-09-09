# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Bassoon(Instrument):
    r'''A bassoon.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> bassoon = instrumenttools.Bassoon()
        >>> attach(bassoon, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Bassoon }
            \set Staff.shortInstrumentName = \markup { Bsn. }
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
        instrument_name='bassoon',
        short_instrument_name='bsn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass', 'tenor'),
        pitch_range='[Bb1, Eb5]',
        sounding_pitch_of_written_middle_c=None,
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
        self._starting_clefs = indicatortools.ClefInventory(['bass'])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bassoon's allowable clefs.

        ..  container:: example

            ::

                >>> bassoon.allowable_clefs
                ClefInventory([Clef(name='bass'), Clef(name='tenor')])

            ::

                >>> show(bassoon.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets bassoon's name.

        ..  container:: example

            ::

                >>> bassoon.instrument_name
                'bassoon'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets bassoon's instrument name markup.

        ..  container:: example

            ::

                >>> bassoon.instrument_name_markup
                Markup(contents=('Bassoon',))

            ::

                >>> show(bassoon.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bassoon's range.

        ..  container:: example

            ::

                >>> bassoon.pitch_range
                PitchRange(range_string='[Bb1, Eb5]')

            ::

                >>> show(bassoon.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets bassoon's short instrument name.

        ..  container:: example

            ::

                >>> bassoon.short_instrument_name
                'bsn.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets bassoon's short instrument name markup.

        ..  container:: example

            ::

                >>> bassoon.short_instrument_name_markup
                Markup(contents=('Bsn.',))

            ::

                >>> show(bassoon.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of bassoon's written middle C.

        ..  container:: example

            ::

                >>> bassoon.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(bassoon.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
