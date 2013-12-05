# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Guitar(Instrument):
    r'''A guitar.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> guitar = instrumenttools.Guitar()
        >>> attach(guitar, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Guitar }
            \set Staff.shortInstrumentName = \markup { Gt. }
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
        instrument_name='guitar',
        short_instrument_name='gt.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='c',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-20, 16)
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
            'string player',
            'guitarist',
            ])
        self._is_primary_instrument = True
