from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class Piccolo(Flute):
    r'''.. versionadded:: 2.0

    Abjad model of the piccolo::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Piccolo()(staff)
        Piccolo()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Piccolo }
            \set Staff.shortInstrumentName = \markup { Picc. }
            c'8
            d'8
            e'8
            f'8
        }

    The piccolo targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Flute.__init__(self, **kwargs)
        self._default_instrument_name = 'piccolo'
        self._default_short_instrument_name = 'picc.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("c''")
        self._traditional_pitch_range = pitchtools.PitchRange(14, 48)
