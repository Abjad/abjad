from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._KeyboardInstrument import _KeyboardInstrument
from abjad.tools.instrumenttools._ReedInstrument import _ReedInstrument


# TODO: figure out why resolution of effective context as staff group isn't working
class Accordion(_KeyboardInstrument, _ReedInstrument):
    r'''.. versionadded 1.1.2

    Abjad model of the accordion::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Accordion(target_context = Staff)(staff)
        Accordion()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Accordion }
            \set Staff.shortInstrumentName = \markup { Acc. }
            c'8
            d'8
            e'8
            f'8
        }

    The accordion targets piano staff context by default.
    '''

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        _KeyboardInstrument.__init__(self, target_context=target_context, **kwargs)
        self._default_instrument_name = 'accordion'
        self._default_performer_names.append('accordionist')
        self._default_short_instrument_name = 'acc.'
        self._is_primary_instrument = True
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-32, 48)
