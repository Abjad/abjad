from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.KeyboardInstrument import KeyboardInstrument
from abjad.tools.instrumenttools.ReedInstrument import ReedInstrument


class Accordion(KeyboardInstrument, ReedInstrument):
    r'''.. versionadded 1.1.2

    Abjad model of the accordion::

        >>> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        >>> instrumenttools.Accordion()(piano_staff)
        Accordion()(PianoStaff<<2>>)

    ::

        >>> f(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Accordion }
            \set PianoStaff.shortInstrumentName = \markup { Acc. }
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

    ::

        >>> show(piano_staff) # doctest: +SKIP

    The accordion targets piano staff context by default.
    '''

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        KeyboardInstrument.__init__(self, target_context=target_context, **kwargs)
        self._default_instrument_name = 'accordion'
        self._default_performer_names.append('accordionist')
        self._default_short_instrument_name = 'acc.'
        self._is_primary_instrument = True
        self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-32, 48)

    ### READ-ONLY PRIVATE PROPERTIES ###

    # TODO: extend class definition to allow for custom target context in repr
    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return ()
