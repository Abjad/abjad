# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Bassoon(Instrument):
    r'''A bassoon.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = contexttools.ClefMark('bass')
        >>> clef = clef.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ::

        >>> bassoon = instrumenttools.Bassoon()
        >>> bassoon = bassoon.attach(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Bassoon }
            \set Staff.shortInstrumentName = \markup { Bsn. }
            c'8
            d'8
            e'8
            f'8
        }

    The bassoon targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_allowable_clefs = contexttools.ClefMarkInventory([
            contexttools.ClefMark('bass'), 
            contexttools.ClefMark('tenor'),
            ])
        self._default_instrument_name = 'bassoon'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'double reed player',
            'bassoonist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-26, 15)
        self._default_short_instrument_name = 'bsn.'
        self._default_starting_clefs = contexttools.ClefMarkInventory([
            contexttools.ClefMark('bass'),
            ])
        self._is_primary_instrument = True
