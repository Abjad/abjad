# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Cello(Instrument):
    r'''A cello.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = Clef('bass')
        >>> attach(clef, staff)
        >>> cello = instrumenttools.Cello()
        >>> attach(cello, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Cello }
            \set Staff.shortInstrumentName = \markup { Vc. }
            c'8
            d'8
            e'8
            f'8
        }

    The cello targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_allowable_clefs = indicatortools.ClefInventory([
            indicatortools.Clef('bass'),
            indicatortools.Clef('tenor'),
            indicatortools.Clef('treble'),
            ])
        self._default_instrument_name = 'cello'
        self._default_performer_names.extend([
            'string player',
            'cellist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-24, 19)
        self._default_short_instrument_name = 'vc.'
        self._default_starting_clefs = [indicatortools.Clef('bass')]
        self._is_primary_instrument = True
