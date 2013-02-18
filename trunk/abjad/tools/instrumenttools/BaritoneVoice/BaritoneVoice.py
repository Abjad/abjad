from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Voice import Voice


class BaritoneVoice(Voice):
    r'''.. versionadded:: 2.8

    Abjad model of the baritone voice::

        >>> staff = Staff("c8 d8 e8 f8")

    ::

        >>> instrumenttools.BaritoneVoice()(staff)
        BaritoneVoice()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Baritone voice }
            \set Staff.shortInstrumentName = \markup { Baritone }
            c8
            d8
            e8
            f8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The baritone voice targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Voice.__init__(self, **kwargs)
        self._default_instrument_name = 'baritone voice'
        self._default_performer_names.append('baritone')
        self._default_short_instrument_name = 'baritone'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(('A2', 'A4'))
