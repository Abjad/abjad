from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Guitar(_StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the guitar::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Guitar()(staff)
        Guitar()(Staff{4})

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

    def __init__(self, **kwargs):
        _StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'guitar'
        self._default_performer_names.append('guitarist')
        self._default_short_instrument_name = 'gt.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-20, 16)
