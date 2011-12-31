from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Trombone._Trombone import _Trombone


class TenorTrombone(_Trombone):
    r'''.. versionadded:: 2.0

    Abjad model of the tenor trombone::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        abjad> instrumenttools.TenorTrombone()(staff)
        TenorTrombone()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tenor trombone }
            \set Staff.shortInstrumentName = \markup { Ten. trb. }
            c'8
            d'8
            e'8
            f'8
        }

    The tenor trombone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Trombone.__init__(self, **kwargs)
        self._default_instrument_name = 'tenor trombone'
        self._default_short_instrument_name = 'ten. trb.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-20, 15)
