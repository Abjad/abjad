# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabassoon(Instrument):
    r'''A contrabassoon.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = contexttools.ClefMark('bass')
        >>> clef.attach(staff)
        ClefMark('bass')(Staff{4})
        >>> contrabassoon = instrumenttools.Contrabassoon()
        >>> contrabassoon.attach(staff)
        Contrabassoon()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Contrabassoon }
            \set Staff.shortInstrumentName = \markup { Contrabsn. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabassoon targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabassoon'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'double reed player',
            'bassoonist',
            ])
        self._default_short_instrument_name = 'contrabsn.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('c')
        self._starting_clefs = [contexttools.ClefMark('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-38, -2)
