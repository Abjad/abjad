from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class BassFlute(Flute):
    r'''.. versionadded:: 2.0

    Abjad model of the bass flute::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.BassFlute()(staff)
        BassFlute()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass flute }
            \set Staff.shortInstrumentName = \markup { Bass fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The bass flute targets staff context by default.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None,
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        Flute.__init__(self, instrument_name, short_instrument_name,
            instrument_name_markup=instrument_name_markup, 
            short_instrument_name_markup=short_instrument_name_markup, target_context=target_context)
        self._default_instrument_name = 'bass flute'
        self._default_short_instrument_name = 'bass fl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
        self.traditional_range = (-12, 24)
