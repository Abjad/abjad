# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class EFlatClarinet(Instrument):
    r'''A E-flat clarinet.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = instrumenttools.EFlatClarinet()
        >>> attach(clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in E-flat }
            \set Staff.shortInstrumentName = \markup { Cl. E-flat }
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
        instrument_name='clarinet in E-flat',
        short_instrument_name='cl. E-flat',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c="ef'",
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-7, 36)
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
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
