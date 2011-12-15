from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._WindInstrument import _WindInstrument


class Flute(_WindInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the flute::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Flute()(staff)
        Flute()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The flute targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _WindInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'flute'
        self._default_performer_names.extend(['flautist', 'flutist'])
        self._default_short_instrument_name = 'fl.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(0, 38)
