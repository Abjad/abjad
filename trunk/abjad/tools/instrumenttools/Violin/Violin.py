from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Violin(_StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the violin::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Violin( )(staff)
        Violin('Violin', 'Vn.')

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin }
            \set Staff.shortInstrumentName = \markup { Vn. }
            c'8
            d'8
            e'8
            f'8
        }

    The violin targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Violin', short_instrument_name = 'Vn.', target_context = None):
        _StringInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs( )
        self.traditional_range = (-5, 43)
