from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Saxophone.Saxophone import Saxophone


class TenorSaxophone(Saxophone):
    r'''.. versionadded:: 2.6

    Abjad model of the tenor saxophone::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.TenorSaxophone()(staff)
        TenorSaxophone()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Tenor saxophone }
            \set Staff.shortInstrumentName = \markup { Ten. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The tenor saxophone is pitched in B-flat.

    The tenor saxophone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'tenor saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'ten. sax.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf,')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-16, 16)
