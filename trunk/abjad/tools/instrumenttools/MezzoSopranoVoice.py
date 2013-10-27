# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class MezzoSopranoVoice(Instrument):
    r'''A mezzo-soprano voice.

    ::

        >>> staff = Staff("c''8 d''8 e''8 f''8")

    ::

        >>> instrumenttools.MezzoSopranoVoice()(staff)
        MezzoSopranoVoice()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Mezzo-soprano voice }
            \set Staff.shortInstrumentName = \markup { Mezzo-soprano }
            c''8
            d''8
            e''8
            f''8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The mezzo-soprano voice targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    default_performer_abbreviation = 'ms.'

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'mezzo-soprano voice'
        self._default_performer_names.extend([
            'vocalist',
            'mezzo-soprano',
            ])
        self._default_short_instrument_name = 'mezzo-soprano'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(('A3', 'C6'))
