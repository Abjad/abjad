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
            \set Staff.instrumentName = \markup { Alto flute }
            \set Staff.shortInstrumentName = \markup { Alt. fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The alto flute targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Flute.__init__(self, **kwargs)
        self._default_instrument_name = 'alto flute'
        self._default_short_instrument_name = 'alt. fl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("g")
        self._traditional_pitch_range = pitchtools.PitchRange(-5, 31)
