# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Cello(Instrument):
    r'''A cello.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = Clef('bass')
        >>> attach(clef, staff)
        >>> cello = instrumenttools.Cello()
        >>> attach(cello, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Cello }
            \set Staff.shortInstrumentName = \markup { Vc. }
            c'8
            d'8
            e'8
            f'8
        }

    The cello targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='cello',
        short_instrument_name='vc.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-24, 19)
        allowable_clefs = allowable_clefs or indicatortools.ClefInventory([
            indicatortools.Clef('bass'),
            indicatortools.Clef('tenor'),
            indicatortools.Clef('treble'),
            ])
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
            'cellist',
            ])
        self._starting_clefs = indicatortools.ClefInventory(['bass'])
        self._is_primary_instrument = True
