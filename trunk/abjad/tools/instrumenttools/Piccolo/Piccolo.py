# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class Piccolo(Flute):
    r'''Abjad model of the piccolo:

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
        Flute.__init__(self, **kwargs)
        self._default_instrument_name = 'piccolo'
        self._default_short_instrument_name = 'picc.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedChromaticPitch("c''")
        self._traditional_pitch_range = pitchtools.PitchRange(14, 48)
