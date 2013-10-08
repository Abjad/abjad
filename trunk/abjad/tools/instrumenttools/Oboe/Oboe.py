# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.DoubleReedInstrument \
	import DoubleReedInstrument


class Oboe(DoubleReedInstrument):
    r'''Abjad model of the oboe:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Oboe()(staff)
        Oboe()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Oboe }
            \set Staff.shortInstrumentName = \markup { Ob. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The oboe targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        DoubleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'oboe'
        self._default_performer_names.append('oboist')
        self._default_short_instrument_name = 'ob.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-2, 33)
