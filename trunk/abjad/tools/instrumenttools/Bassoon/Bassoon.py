from abjad.tools import contexttools
from abjad.tools.instrumenttools._DoubleReedInstrument import _DoubleReedInstrument


class Bassoon(_DoubleReedInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the bassoon::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        abjad> instrumenttools.Bassoon()(staff)
        Bassoon('Bassoon', 'Bsn.')

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

    def __init__(self,
        instrument_name = 'Bassoon', short_instrument_name = 'Bsn.', target_context = None):
        _DoubleReedInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self.all_clefs = [contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
        self.traditional_range = (-26, 15)
