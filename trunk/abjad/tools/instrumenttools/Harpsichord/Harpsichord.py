from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._KeyboardInstrument import _KeyboardInstrument


class Harpsichord(_KeyboardInstrument):
    r'''.. versionadded:: 2.5

    Abjad model of the harpsichord::

        abjad> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        abjad> instrumenttools.Harpsichord()(piano_staff)
        Harpsichord()(PianoStaff<<2>>)

    ::

        abjad> f(piano_staff) # doctest: +SKIP
        \new PianoStaff <<
            %%% \set Staff.instrumentName = \markup { Harpsichord } %%%
            %%% \set Staff.shortInstrumentName = \markup { Hpschd. } %%%
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                b4
            }
        >>

    The harpsichord targets piano staff context by default.

    Return instrument.
    '''

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        _KeyboardInstrument.__init__(self, target_context=target_context, **kwargs)    
        self._default_instrument_name = 'harpsichord'
        self._default_performer_names.append('harpsichordist')
        self._default_short_instrument_name = 'hpschd.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-24, 36)
