from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Vibraphone(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the vibraphone::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Vibraphone()(staff)
        Vibraphone('Vibraphone', 'Vibr.')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Vibraphone }
            \set Staff.shortInstrumentName = \markup { Vibr. }
            c'8
            d'8
            e'8
            f'8
        }

    The vibraphone targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Vibraphone', short_instrument_name = 'Vibr.', target_context = None):
        _PercussionInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-7, 29)
