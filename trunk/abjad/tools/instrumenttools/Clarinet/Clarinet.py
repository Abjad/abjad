from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._SingleReedInstrument import _SingleReedInstrument


class Clarinet(_SingleReedInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the B-flat clarinet::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Clarinet()(staff)
        Clarinet()(Staff{4})

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

    def __init__(self, instrument_name=None, short_instrument_name=None,
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        _SingleReedInstrument.__init__(self, instrument_name, short_instrument_name,
            instrument_name_markup=instrument_name_markup, 
            short_instrument_name_markup=short_instrument_name_markup, target_context=target_context)
        self._default_instrument_name = 'clarinet'
        self._default_short_instrument_name = 'cl.'
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-10, 34)
