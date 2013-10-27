# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Vibraphone(Instrument):
    r'''A vibraphone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Vibraphone()(staff)
        Vibraphone()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Vibraphone }
            \set Staff.shortInstrumentName = \markup { Vibr. }
            c'8
            d'8
            e'8
            f'8
        }

    The vibraphone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'vibraphone'
        self._default_performer_names.extend([
            'percussionist',
            'vibraphonist',
            ])
        self._default_short_instrument_name = 'vibr.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-7, 29)
