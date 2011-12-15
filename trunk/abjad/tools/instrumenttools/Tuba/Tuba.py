from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument


class Tuba(_BrassInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the tuba::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        abjad> instrumenttools.Tuba()(staff)
        Tuba()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tuba }
            \set Staff.shortInstrumentName = \markup { Tb. }
            c'8
            d'8
            e'8
            f'8
        }

    The tuba targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _BrassInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'tuba'
        self._default_performer_names.append('tubist')
        self._default_short_instrument_name = 'tb.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-34, 5)
