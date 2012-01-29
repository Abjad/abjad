from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Saxophone._Saxophone import _Saxophone


class BassSaxophone(_Saxophone):
    r'''.. versionadded:: 2.6

    Abjad model of the bass saxophone::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.BassSaxophone()(staff)
        BassSaxophone()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass saxophone }
            \set Staff.shortInstrumentName = \markup { Bass sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The bass saxophone is pitched in B-flat.

    The bass saxophone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'bass saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'bass sax.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf,,')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-28, 4)
