# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassVoice(Instrument):
    r'''A bass.

    ::

        >>> staff = Staff("c8 d8 e8 f8")
        >>> bass = instrumenttools.BassVoice()
        >>> attach(bass, staff)

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass }
            \set Staff.shortInstrumentName = \markup { Bass }
            c8
            d8
            e8
            f8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The bass voice targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='bass',
        short_instrument_name='bass',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        allowable_clefs = indicatortools.ClefInventory(['bass'])
        pitch_range = pitch_range = pitchtools.PitchRange('[E2, F4]')
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
            'vocalist',
            'bass',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['bass'])
