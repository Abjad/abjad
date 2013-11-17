# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


# TODO: extend class definition to allow for custom target context in repr
class Piano(Instrument):
    r'''A piano.

    ::

        >>> piano_staff = scoretools.PianoStaff()
        >>> piano_staff.append(Staff("c'8 d'8 e'8 f'8"))
        >>> piano_staff.append(Staff("c'4 b4"))

    ::

        >>> piano = instrumenttools.Piano()
        >>> attach(piano, piano_staff)
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(piano_staff)
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

    The piano targets piano staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_scope = scoretools.PianoStaff
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
            indicatortools.Clef('treble'), indicatortools.Clef('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-39, 48)

