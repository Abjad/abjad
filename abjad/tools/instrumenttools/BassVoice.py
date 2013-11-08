# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassVoice(Instrument):
    r'''A bass.

    ::

        >>> staff = Staff("c8 d8 e8 f8")
        >>> bass = instrumenttools.BassVoice()
        >>> attach(bass, staff)
        BassVoice()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass voice }
            \set Staff.shortInstrumentName = \markup { Bass }
            c8
            d8
            e8
            f8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The bass voice targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'bass voice'
        self._default_performer_names.extend([
            'vocalist',
            'bass',
            ])
        self._default_short_instrument_name = 'bass'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [marktools.Clef('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(('E2', 'F4'))
