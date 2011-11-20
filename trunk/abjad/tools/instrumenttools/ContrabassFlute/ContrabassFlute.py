from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class ContrabassFlute(Flute):
    r'''.. versionadded:: 2.0

    Abjad model of the contrabass flute::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.ContrabassFlute()(staff)
        ContrabassFlute()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass Flute }
            \set Staff.shortInstrumentName = \markup { Cbass Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass flute targets staff context by default.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None, 
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        Flute.__init__(self, instrument_name, short_instrument_name,
            instrument_name_markup=instrument_name_markup, 
            short_instrument_name_markup=short_instrument_name_markup, target_context=target_context)
        self._default_instrument_name = 'contrabass flute'
        self._default_short_instrument_name = 'cbass. fl.'
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('g,')
        self.traditional_range = (-17, 19)
