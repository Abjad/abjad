# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.StringInstrument import StringInstrument


class Contrabass(StringInstrument):
    r'''Abjad model of the contrabass:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        >>> instrumenttools.Contrabass()(staff)
        Contrabass()(Staff{4})

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

    ::

        >>> show(staff) # doctest: +SKIP

    The contrabass targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass'
        self._default_performer_names.extend(['contrabassist', 'bassist'])
        self._default_short_instrument_name = 'vb.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('c')
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self.all_clefs = [
            contexttools.ClefMark('bass'), contexttools.ClefMark('treble')]
        self._default_pitch_range = pitchtools.PitchRange(-32, 2)
