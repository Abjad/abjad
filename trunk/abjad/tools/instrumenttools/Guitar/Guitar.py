from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Guitar(_StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the guitar::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Guitar( )(staff)
        Guitar('Guitar', 'Gt.')

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Guitar }
            \set Staff.shortInstrumentName = \markup { Gt. }
            c'8
            d'8
            e'8
            f'8
        }

    The guitar targets staff context by default.
    '''

    def __init__(self,
        instrument_name = 'Guitar', short_instrument_name = 'Gt.', target_context = None):
        _StringInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs( )
        self.traditional_range = (-20, 16)
