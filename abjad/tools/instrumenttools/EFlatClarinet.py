# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class EFlatClarinet(Instrument):
    r'''A E-flat clarinet.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clarinet = instrumenttools.EFlatClarinet()
        >>> attach(clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in E-flat }
            \set Staff.shortInstrumentName = \markup { Cl. E-flat }
            c'8
            d'8
            e'8
            f'8
        }

    The E-flat clarinet targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'clarinet in E-flat'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._default_short_instrument_name = 'cl. E-flat'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("ef'")
        self._starting_clefs = [marktools.Clef('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-7, 36)
