from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._DoubleReedInstrument import _DoubleReedInstrument


class Oboe(_DoubleReedInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the oboe::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Oboe( )(staff)
        Oboe('Oboe', 'Ob.')

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Oboe }
            \set Staff.shortInstrumentName = \markup { Ob. }
            c'8
            d'8
            e'8
            f'8
        }

    The oboe targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Oboe', short_instrument_name = 'Ob.', target_context = None):
        _DoubleReedInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs( )
        self.traditional_range = (-2, 33)
