# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabassoon(Instrument):
    r'''A contrabassoon.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef('bass')
        >>> attach(clef, staff)
        >>> contrabassoon = instrumenttools.Contrabassoon()
        >>> attach(contrabassoon, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
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
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='c',
        ):
        allowable_clefs = indicatortools.ClefInventory(['bass'])
        pitch_range = pitch_range or pitchtools.PitchRange(-38, -2)
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
