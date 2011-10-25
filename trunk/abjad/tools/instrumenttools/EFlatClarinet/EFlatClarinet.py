from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Clarinet import Clarinet


class EFlatClarinet(Clarinet):
    r'''.. versionadded:: 2.0

    Abjad model of the E-flat clarinet::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.EFlatClarinet()(staff)
        EFlatClarinet()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in E-flat }
            \set Staff.shortInstrumentName = \markup { Cl. E-flat }
            c'8
            d'8
            e'8
            f'8
        }

    The E-flat clarinet targets staff context by default.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None, target_context=None):
        Clarinet.__init__(self, instrument_name, short_instrument_name, target_context)
        self._default_instrument_name = markuptools.Markup('Clarinet in E-flat')
        self._default_short_instrument_name = markuptools.Markup('Cl. E-flat')
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("ef'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-7, 36)
