from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Marimba(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the marimba::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Marimba()(staff)
        Marimba('Marimba', 'Mb.')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Marimba }
            \set Staff.shortInstrumentName = \markup { Mb. }
            c'8
            d'8
            e'8
            f'8
        }

    The marimba targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Marimba', short_instrument_name = 'Mb.', target_context = None):
        _PercussionInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-19, 36)
