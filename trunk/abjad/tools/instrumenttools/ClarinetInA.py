# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ClarinetInA(Instrument):
    r'''A clarinet in A.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clarinet = instrumenttools.ClarinetInA()
        >>> attach(clarinet, staff)
        ClarinetInA()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in A }
            \set Staff.shortInstrumentName = \markup { Cl. A \natural }
            c'8
            d'8
            e'8
            f'8
        }

    The clarinet in A targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('a')
        self._default_instrument_name = 'clarinet in A'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._default_short_instrument_name = r'cl. A \natural'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = [marktools.ClefMark('treble')]
        self._default_pitch_range = pitchtools.PitchRange(-11, 33)
        self._is_primary_instrument = False
        self._copy_default_starting_clefs_to_default_allowable_clefs()
