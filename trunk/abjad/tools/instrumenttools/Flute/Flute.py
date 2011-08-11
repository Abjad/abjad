from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._WindInstrument import _WindInstrument


class Flute(_WindInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the flute::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Flute( )(staff)
        Flute('Flute', 'Fl.')

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The flute targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Flute', short_instrument_name = 'Fl.', target_context = None):
        _WindInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs( )
        self.traditional_range = (0, 38)
