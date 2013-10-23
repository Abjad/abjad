# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


# TODO: extend class definition to allow for custom target context in repr
class Piano(Instrument):
    r'''A piano.

    ::

        >>> piano_staff = scoretools.PianoStaff(
        ...     [Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        >>> instrumenttools.Piano()(piano_staff)
        Piano()(PianoStaff<<2>>)

    ..  doctest::

        >>> f(piano_staff)
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

    ::

        >>> show(piano_staff) # doctest: +SKIP

    The piano targets piano staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        Instrument.__init__(
            self, 
            target_context=target_context, 
            **kwargs
            )
        self._default_instrument_name = 'piano'
        self._default_performer_names.extend([
            'keyboardist',
            'pianist',
            ])
        self._default_short_instrument_name = 'pf.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [
            contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-39, 48)

    ### PRIVATE PROPERTIES ###

    # TODO: extend class definition to allow for custom target context in repr
    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return ()
