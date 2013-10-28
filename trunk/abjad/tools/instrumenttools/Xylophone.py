# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Xylophone(Instrument):
    r'''A xylphone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> xylophone = instrumenttools.Xylophone()
        >>> attach(xylophone, staff)
        Xylophone()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Xylophone }
            \set Staff.shortInstrumentName = \markup { Xyl. }
            c'8
            d'8
            e'8
            f'8
        }

    The xylophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'xylophone'
        self._default_performer_names.extend([
            'percussionist',
            'xylophonist',
            ])
        self._default_short_instrument_name = 'xyl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c''")
        self._starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(0, 36)
