from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Saxophone.Saxophone import Saxophone


class AltoSaxophone(Saxophone):
    r'''.. versionadded:: 2.6

    Abjad model of the alto saxophone::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.AltoSaxophone()(staff)
        AltoSaxophone()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto saxophone }
            \set Staff.shortInstrumentName = \markup { Alto sax. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The alto saxophone is pitched in E-flat.

    The alto saxophone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'alto saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'alto sax.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('ef')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-11, 21)
