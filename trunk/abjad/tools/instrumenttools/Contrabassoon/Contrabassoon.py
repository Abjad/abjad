from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Bassoon import Bassoon


class Contrabassoon(Bassoon):
    r'''.. versionadded:: 2.0

    Abjad model of the contrabassoon::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        abjad> instrumenttools.Contrabassoon()(staff)
        Contrabassoon()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Contrabassoon }
            \set Staff.shortInstrumentName = \markup { Contrabsn. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabassoon targets staff context by default.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None, target_context=None):
        Bassoon.__init__(self, instrument_name, short_instrument_name, target_context)
        self._default_instrument_name = markuptools.Markup('Contrabassoon')
        self._default_short_instrument_name = markuptools.Markup('Contrabsn.')
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-38, -2)
