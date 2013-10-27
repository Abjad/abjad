# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Piccolo(Instrument):
    r'''A piccolo.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Piccolo()(staff)
        Piccolo()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Piccolo }
            \set Staff.shortInstrumentName = \markup { Picc. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The piccolo targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch("c''")
        self._default_instrument_name = 'piccolo'
        self._default_performer_names.extend([
            'wind player',
            'flautist',
            'flutist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(14, 48)
        self._default_short_instrument_name = 'picc.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = [contexttools.ClefMark('treble')]
        self._is_primary_instrument = False
        self._copy_default_starting_clefs_to_default_allowable_clefs()
