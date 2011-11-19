from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._KeyboardInstrument import _KeyboardInstrument


class Piano(_KeyboardInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the piano::

        abjad> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        abjad> instrumenttools.Piano()(piano_staff)
        Piano()(PianoStaff<<2>>)

    ::

        abjad> f(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Piano }
            \set PianoStaff.shortInstrumentName = \markup { Pf. }
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

    The piano target piano staff context by default.
    '''

    def __init__(self, instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        if target_context is None:
            target_context = scoretools.PianoStaff
        _KeyboardInstrument.__init__(self, instrument_name_markup, short_instrument_name_markup, target_context)
        self._default_instrument_name_markup = markuptools.Markup('Piano')
        self._default_short_instrument_name_markup = markuptools.Markup('Pf.')
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-39, 48)
