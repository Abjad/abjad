from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Voice import _Voice


class ContraltoVoice(_Voice):
    r'''.. versionadded:: 2.8

    Abjad model of the contralto voice::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.ContraltoVoice()(staff)
        ContraltoVoice()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contralto voice }
            \set Staff.shortInstrumentName = \markup { Contralto }
            c'8
            d'8
            e'8
            f'8
        }

    The contralto voice targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Voice.__init__(self, **kwargs)
        self._default_instrument_name = 'contralto voice'
        self._default_performer_names.append('contralto')
        self._default_short_instrument_name = 'contralto'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(('F3', 'G5'))
