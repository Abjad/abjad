# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorTrombone(Instrument):
    r'''A tenor trombone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef('bass')
        >>> attach(clef, staff)
        >>> trombone = instrumenttools.TenorTrombone()
        >>> attach(trombone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tenor trombone }
            \set Staff.shortInstrumentName = \markup { Ten. trb. }
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
        instrument_name='tenor trombone',
        short_instrument_name='ten. trb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        allowable_clefs = allowable_clefs or indicatortools.ClefInventory(
            ['tenor', 'bass'])
        pitch_range = pitch_range or pitchtools.PitchRange(-20, 15)
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
            'brass player',
            'trombonist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['tenor', 'bass'])
