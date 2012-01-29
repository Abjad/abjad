from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Clarinet._Clarinet import _Clarinet


class BFlatClarinet(_Clarinet):
    r'''.. versionadded:: 2.0

    Abjad model of the B-flat clarinet::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.BFlatClarinet()(staff)
        BFlatClarinet()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            c'8
            d'8
            e'8
            f'8
        }

    The B-flat clarinet targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Clarinet.__init__(self, **kwargs)
        self._default_instrument_name = 'clarinet in B-flat'
        self._default_performer_names.extend(['clarinettist', 'clarinetist'])
        self._default_short_instrument_name = 'cl. in B-flat'
        self._is_primary_instrument = True
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-10, 34)
