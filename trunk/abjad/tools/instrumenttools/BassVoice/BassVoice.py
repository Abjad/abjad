from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Voice import _Voice


class BassVoice(_Voice):
    r'''.. versionadded:: 2.8

    Abjad model of the bass voice::

        >>> staff = Staff("c8 d8 e8 f8")

    ::

        >>> instrumenttools.BassVoice()(staff)
        BassVoice()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass voice }
            \set Staff.shortInstrumentName = \markup { Bass }
            c8
            d8
            e8
            f8
        }

    The bass voice targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Voice.__init__(self, **kwargs)
        self._default_instrument_name = 'bass voice'
        self._default_performer_names.append('bass')
        self._default_short_instrument_name = 'bass'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(('E2', 'F4'))
