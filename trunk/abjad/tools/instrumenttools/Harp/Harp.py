from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Harp(_StringInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the harp::

        abjad> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        abjad> instrumenttools.Harp()(piano_staff)
        Harp()(PianoStaff<<2>>)

    ::

        abjad> f(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Harp }
            \set PianoStaff.shortInstrumentName = \markup { Hp. }
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

    The harp targets piano staff context by default.
    '''

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        _StringInstrument.__init__(self, target_context=target_context, **kwargs)
        self._default_instrument_name = 'harp'
        self._default_performer_names.append('harpist')
        self._default_short_instrument_name = 'hp.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-37, 44)
