from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.StringInstrument import StringInstrument


class Viola(StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the viola::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('alto')(staff)
        ClefMark('alto')(Staff{4})

    ::

        >>> instrumenttools.Viola()(staff)
        Viola()(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \clef "alto"
            \set Staff.instrumentName = \markup { Viola }
            \set Staff.shortInstrumentName = \markup { Va. }
            c'8
            d'8
            e'8
            f'8
        }

    The viola targets staff context by default.
    '''

    def __init__(self, **kwargs):
        StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'viola'
        self._default_performer_names.append('violist')
        self._default_short_instrument_name = 'va.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('alto')]
        self.all_clefs = [
            contexttools.ClefMark('alto'),
            contexttools.ClefMark('treble')]
        self._traditional_pitch_range = pitchtools.PitchRange(-12, 28)
