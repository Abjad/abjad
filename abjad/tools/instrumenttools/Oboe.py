# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Oboe(Instrument):
    r'''An oboe.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> oboe = instrumenttools.Oboe()
        >>> attach(oboe, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Oboe }
            \set Staff.shortInstrumentName = \markup { Ob. }
            c'8
            d'8
            e'8
            f'8
        }

    The oboe targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='oboe',
        short_instrument_name='ob.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-2, 33)
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
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'double reed player',
            'oboist',
            ])
        self._is_primary_instrument = True
