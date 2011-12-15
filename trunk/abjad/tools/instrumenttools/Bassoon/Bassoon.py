from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._DoubleReedInstrument import _DoubleReedInstrument


class Bassoon(_DoubleReedInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the bassoon::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        abjad> instrumenttools.Bassoon()(staff)
        Bassoon()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Bassoon }
            \set Staff.shortInstrumentName = \markup { Bsn. }
            c'8
            d'8
            e'8
            f'8
        }

    The bassoon targets staff context by default.
    '''

    def __init__(self, **kwargs):
        _DoubleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'bassoon'
        self._default_performer_names.append('bassoonist')
        self._default_short_instrument_name = 'bsn.'
        self._is_primary_instrument = True
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self.all_clefs = [contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
        self._traditional_pitch_range = pitchtools.PitchRange(-26, 15)
