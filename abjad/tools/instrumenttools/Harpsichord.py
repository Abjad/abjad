# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class Harpsichord(Instrument):
    r'''A harpsichord.

    ::

        >>> upper_staff = Staff("c'8 d'8 e'8 f'8")
        >>> lower_staff = Staff("c'4 b4")
        >>> piano_staff = scoretools.PianoStaff([upper_staff, lower_staff])

    ::

        >>> harpsichord = instrumenttools.Harpsichord()
        >>> attach(harpsichord, piano_staff)
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(piano_staff)
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

    The harpsichord targets piano staff context by default.

    Returns instrument.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_scope = scoretools.PianoStaff
        self._default_instrument_name = 'harpsichord'
        self._default_performer_names.extend([
            'keyboardist',
            'harpsichordist'
            ])
        self._default_short_instrument_name = 'hpschd.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [
            indicatortools.Clef('treble'), indicatortools.Clef('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-24, 36)
