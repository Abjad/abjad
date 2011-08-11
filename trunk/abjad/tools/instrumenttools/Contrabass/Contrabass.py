from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Contrabass(_StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the contrabass::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        abjad> instrumenttools.Contrabass( )(staff)
        Contrabass('Contrabass', 'Vb.')

    ::

        abjad> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Contrabass }
            \set Staff.shortInstrumentName = \markup { Vb. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Contrabass', short_instrument_name = 'Vb.', target_context = None):
        _StringInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self.all_clefs = [contexttools.ClefMark('bass'), contexttools.ClefMark('treble')]
        self.traditional_range = (-32, 2)
