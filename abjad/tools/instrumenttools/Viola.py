# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Viola(Instrument):
    r'''A viola.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef('alto')
        >>> attach(clef, staff)
        >>> viola = instrumenttools.Viola()
        >>> attach(viola, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \clef "alto"
            \set Staff.instrumentName = \markup { Viola }
            \set Staff.shortInstrumentName = \markup { Va. }
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
        instrument_name='viola',
        short_instrument_name='va.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        allowable_clefs = allowable_clefs or indicatortools.ClefInventory(
            ['alto', 'treble'])
        pitch_range = pitch_range or pitchtools.PitchRange(-12, 28)
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
            'violist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['alto'])
