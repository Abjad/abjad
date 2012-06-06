from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Xylophone(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the xylphone::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Xylophone()(staff)
        Xylophone()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Xylophone }
            \set Staff.shortInstrumentName = \markup { Xyl. }
            c'8
            d'8
            e'8
            f'8
        }

    The xylophone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _PercussionInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'xylophone'
        self._default_performer_names.append('xylophonist')
        self._default_short_instrument_name = 'xyl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("c''")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(0, 36)
