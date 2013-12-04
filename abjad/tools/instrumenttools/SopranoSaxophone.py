# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class SopranoSaxophone(Instrument):
    r'''A soprano saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> sax = instrumenttools.SopranoSaxophone()
        >>> attach(sax, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Soprano saxophone }
            \set Staff.shortInstrumentName = \markup { Sop. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The soprano saxophone is pitched in B-flat.

    The soprano saxophone targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='soprano saxophone',
        short_instrument_name='sop. sax.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='bf',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-4, 28)
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
            'single reed player',
            'saxophonist',
            ])
