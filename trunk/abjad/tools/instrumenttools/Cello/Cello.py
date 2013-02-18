from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.StringInstrument import StringInstrument


class Cello(StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the cello::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        >>> instrumenttools.Cello()(staff)
        Cello()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Cello }
            \set Staff.shortInstrumentName = \markup { Vc. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The cello targets staff context by default.
    '''

    def __init__(self, **kwargs):
        StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'cello'
        self._default_performer_names.append('cellist')
        self._default_short_instrument_name = 'vc.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self.all_clefs = [
            contexttools.ClefMark('bass'),
            contexttools.ClefMark('tenor'),
            contexttools.ClefMark('treble')]
        self._traditional_pitch_range = pitchtools.PitchRange(-24, 19)
