# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassSaxophone(Instrument):
    r'''A bass saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP
        >>> bass_sax = instrumenttools.BassSaxophone()
        >>> bass_sax = attach(bass_sax, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass saxophone }
            \set Staff.shortInstrumentName = \markup { Bass sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The bass saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('bf,,')
        self._default_instrument_name = 'bass saxophone'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])
        self._default_short_instrument_name = 'bass sax.'
        self._default_pitch_range = pitchtools.PitchRange(-28, 4)
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = marktools.ClefMarkInventory([
            marktools.ClefMark('treble'),
            ])
        self._is_primary_instrument = False
        self._copy_default_starting_clefs_to_default_allowable_clefs()
