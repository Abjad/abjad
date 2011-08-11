from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class UntunedPercussion(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of untuned percussion::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.UntunedPercussion( )(staff)
        UntunedPercussion('Percussion', 'Perc.')

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Percussion }
            \set Staff.shortInstrumentName = \markup { Perc. }
            c'8
            d'8
            e'8
            f'8
        }

    Untuned percussion targets the staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Percussion', short_instrument_name = 'Perc.', target_context = None):
        _PercussionInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('percussion')]
        self._copy_primary_clefs_to_all_clefs( )
        self.traditional_range = (-48, 39)
