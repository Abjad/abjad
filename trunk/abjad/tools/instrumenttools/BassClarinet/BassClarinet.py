from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Clarinet.Clarinet import Clarinet


class BassClarinet(Clarinet):
    r'''.. versionadded:: 2.0

    Abjad model of the bass clarinet::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.BassClarinet()(staff)
        BassClarinet()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass clarinet }
            \set Staff.shortInstrumentName = \markup { Bass cl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The bass clarinet targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Clarinet.__init__(self, **kwargs)
        self._default_instrument_name = 'bass clarinet'
        self._default_short_instrument_name = 'bass cl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf,')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self.all_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._traditional_pitch_range = pitchtools.PitchRange(-26, 19)
