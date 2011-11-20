from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class AltoFlute(Flute):
    r'''.. versionadded 1.1.2

    Abjad model of the alto flute::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.AltoFlute()(staff)
        AltoFlute()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto Flute }
            \set Staff.shortInstrumentName = \markup { Alt. Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The alto flute targets staff context by default.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None, 
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        Flute.__init__(self, instrument_name, short_instrument_name, 
            instrument_name_markup=instrument_name_markup, 
            short_instrument_name_markup=short_instrument_name_markup, target_context=target_context)
        self._default_instrument_name = 'alto flute'
        self._default_short_instrument_name = 'alt. fl.'
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("g")
        self.traditional_range = (-5, 31)
