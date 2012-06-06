from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Voice import _Voice


class TenorVoice(_Voice):
    r'''.. versionadded:: 2.8

    Abjad model of the tenor voice::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.TenorVoice()(staff)
        TenorVoice()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Tenor voice }
            \set Staff.shortInstrumentName = \markup { Tenor }
            c'8
            d'8
            e'8
            f'8
        }

    The tenor voice targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Voice.__init__(self, **kwargs)
        self._default_instrument_name = 'tenor voice'
        self._default_performer_names.append('tenor')
        self._default_short_instrument_name = 'tenor'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange('C3', 'D5')
