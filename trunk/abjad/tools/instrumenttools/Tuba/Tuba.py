# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Tuba(Instrument):
    r'''A tuba.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        >>> instrumenttools.Tuba()(staff)
        Tuba()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tuba }
            \set Staff.shortInstrumentName = \markup { Tb. }
            c'8
            d'8
            e'8
            f'8
        }

    The tuba targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'tuba'
        self._default_performer_names.extend([
            'brass player',
            'tubist',
            ])
        self._default_short_instrument_name = 'tb.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [contexttools.ClefMark('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-34, 5)
        #self._make_default_name_markups()
