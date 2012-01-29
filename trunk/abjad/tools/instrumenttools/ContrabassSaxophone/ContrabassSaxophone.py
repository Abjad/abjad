from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._Saxophone._Saxophone import _Saxophone


class ContrabassSaxophone(_Saxophone):
    r'''.. versionadded:: 2.6

    Abjad model of the bass saxophone::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.ContrabassSaxophone()(staff)
        ContrabassSaxophone()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass saxophone }
            \set Staff.shortInstrumentName = \markup { Cbass. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass saxophone is pitched in E-flat.

    The contrabass saxophone targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'cbass. sax.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('ef,,')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-36, -4)
