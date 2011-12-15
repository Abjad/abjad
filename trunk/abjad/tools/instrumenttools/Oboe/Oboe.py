from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._DoubleReedInstrument import _DoubleReedInstrument


class Oboe(_DoubleReedInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the oboe::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Oboe()(staff)
        Oboe()(Staff{4})

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

    def __init__(self, **kwargs):
        _DoubleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'oboe'
        self._default_performer_names.append('oboist')
        self._default_short_instrument_name = 'ob.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-2, 33)
