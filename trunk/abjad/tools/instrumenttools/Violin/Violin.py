from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.StringInstrument import StringInstrument


class Violin(StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the violin::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Violin()(staff)
        Violin()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin }
            \set Staff.shortInstrumentName = \markup { Vn. }
            c'8
            d'8
            e'8
            f'8
        }

    The violin targets staff context by default.
    '''

    def __init__(self, **kwargs):
        StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'violin'
        self._default_performer_names.append('violinist')
        self._default_short_instrument_name = 'vn.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-5, 43)
