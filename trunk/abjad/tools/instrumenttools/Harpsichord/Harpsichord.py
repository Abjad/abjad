# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class Harpsichord(Instrument):
    r'''Abjad model of the harpsichord:

    ::

        >>> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        >>> instrumenttools.Harpsichord()(piano_staff)
        Harpsichord()(PianoStaff<<2>>)

    ..  doctest::

        >>> f(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Harpsichord }
            \set PianoStaff.shortInstrumentName = \markup { Hpschd. }
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

    The harpsichord targets piano staff context by default.

    Return instrument.
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
        self._default_instrument_name = 'harpsichord'
        self._default_performer_names.extend([
            'keyboardist',
            'harpsichordist'
            ])
        self._default_short_instrument_name = 'hpschd.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self.starting_clefs = [
            contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-24, 36)
