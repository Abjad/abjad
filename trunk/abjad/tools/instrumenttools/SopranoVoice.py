# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class SopranoVoice(Instrument):
    r'''A soprano voice.

    ::

        >>> staff = Staff("c''8 d''8 e''8 f''8")
        >>> soprano = instrumenttools.SopranoVoice()
        >>> attach(soprano, staff)
        SopranoVoice()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Soprano voice }
            \set Staff.shortInstrumentName = \markup { Soprano }
            c''8
            d''8
            e''8
            f''8
        }

    The soprano voice targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    default_performer_abbreviation = 'sop.'

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'soprano voice'
        self._default_performer_names.extend([
            'vocalist',
            'soprano'
            ])
        self._default_short_instrument_name = 'soprano'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(('C4', 'E6'))
