from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Vibraphone(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the vibraphone::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Vibraphone()(staff)
        Vibraphone()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Vibraphone }
            \set Staff.shortInstrumentName = \markup { Vibr. }
            c'8
            d'8
            e'8
            f'8
        }

    The vibraphone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _PercussionInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'vibraphone'
        self._default_performer_names.append('vibraphonist')
        self._default_short_instrument_name = 'vibr.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-7, 29)
