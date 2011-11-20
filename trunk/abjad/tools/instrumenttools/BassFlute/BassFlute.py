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
            \set Staff.instrumentName = \markup { Bass Flute }
            \set Staff.shortInstrumentName = \markup { Bass Fl. }
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
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
        self.traditional_range = (-12, 24)
