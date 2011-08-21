from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._SingleReedInstrument import _SingleReedInstrument


class Clarinet(_SingleReedInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the B-flat clarinet::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Clarinet()(staff)
        Clarinet('Clarinet', 'Cl.')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet }
            \set Staff.shortInstrumentName = \markup { Cl. }
            c'8
            d'8
            e'8
            f'8
        }

    The clarinet targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Clarinet', short_instrument_name = 'Cl.', target_context = None):
        _SingleReedInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-10, 34)
