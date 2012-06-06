from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Voice import _Voice


class SopranoVoice(_Voice):
    r'''.. versionadded:: 2.8

    Abjad model of the soprano voice::

        >>> staff = Staff("c''8 d''8 e''8 f''8")

    ::

        >>> instrumenttools.SopranoVoice()(staff)
        SopranoVoice()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Soprano voice }
            \set Staff.shortInstrumentName = \markup { Soprano }
            c''8
            d''8
            e''8
            f''8
        }

    The soprano voice targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Voice.__init__(self, **kwargs)
        self._default_instrument_name = 'soprano voice'
        self._default_performer_names.append('soprano')
        self._default_short_instrument_name = 'soprano'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(('C4', 'E6'))
