from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class ContrabassFlute(Flute):
    r'''.. versionadded:: 2.0

    Abjad model of the contrabass flute::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.ContrabassFlute()(staff)
        ContrabassFlute()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass flute }
            \set Staff.shortInstrumentName = \markup { Cbass. fl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The contrabass flute targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Flute.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass flute'
        self._default_short_instrument_name = 'cbass. fl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('g,')
        self._traditional_pitch_range = pitchtools.PitchRange(-17, 19)
