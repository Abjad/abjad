# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassTrombone(Instrument):
    r'''A bass trombone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = Clef('bass')
        >>> attach(clef, staff)
        >>> trombone = instrumenttools.BassTrombone()
        >>> attach(trombone, staff)

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Bass trombone }
            \set Staff.shortInstrumentName = \markup { Bass trb. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The tenor trombone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'bass trombone'
        self._default_performer_names.extend([
            'brass player',
            'trombonist',
            ])
        self._default_short_instrument_name = 'bass trb.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [indicatortools.Clef('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange('[C2, F4]')
