from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Clarinet._Clarinet import _Clarinet


class ClarinetInA(_Clarinet):
    r'''.. versionadded:: 2.6

    Abjad model of the clarinet in A::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.ClarinetInA()(staff)
        ClarinetInA()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in A }
            \set Staff.shortInstrumentName = \markup { Cl. A \natural }
            c'8
            d'8
            e'8
            f'8
        }

    The clarinet in A targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Clarinet.__init__(self, **kwargs)
        self._default_instrument_name = 'clarinet in A'
        self._default_performer_names.extend(['clarinettist', 'clarinetist'])
        self._default_short_instrument_name = r'cl. A \natural'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('a')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-11, 33)
