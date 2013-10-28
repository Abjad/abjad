# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabass(Instrument):
    r'''A contrabass.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = contexttools.ClefMark('bass')
        >>> clef.attach(staff)
        ClefMark('bass')(Staff{4})
        >>> contrabass = instrumenttools.Contrabass()
        >>> contrabass.attach(staff)
        Contrabass()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Contrabass }
            \set Staff.shortInstrumentName = \markup { Vb. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass'
        self._default_performer_names.extend([
            'string player',
            'contrabassist', 
            'bassist',
            ])
        self._default_short_instrument_name = 'vb.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('c')
        self._starting_clefs = [contexttools.ClefMark('bass')]
        self.allowable_clefs = [
            contexttools.ClefMark('bass'), contexttools.ClefMark('treble')]
        self._default_pitch_range = pitchtools.PitchRange(-32, 2)
