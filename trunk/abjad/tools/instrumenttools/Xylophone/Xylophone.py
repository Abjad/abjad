from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Xylophone(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the xylphone::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Xylophone()(staff)
        Xylophone()(Staff{4})

    ::

        abjad> f(staff)
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

    def __init__(self, instrument_name=None, short_instrument_name=None, target_context=None):
        _PercussionInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self._default_instrument_name = markuptools.Markup('Xylophone')
        self._default_short_instrument_name = markuptools.Markup('Xyl.')
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("c''")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (0, 36)
