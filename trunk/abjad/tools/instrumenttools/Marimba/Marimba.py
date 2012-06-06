from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Marimba(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the marimba::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Marimba()(staff)
        Marimba()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Marimba }
            \set Staff.shortInstrumentName = \markup { Mb. }
            c'8
            d'8
            e'8
            f'8
        }

    The marimba targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _PercussionInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'marimba'
        self._default_short_instrument_name = 'mb.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-19, 36)
