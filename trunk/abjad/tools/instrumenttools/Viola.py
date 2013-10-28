# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Viola(Instrument):
    r'''A viola.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = contexttools.ClefMark('alto')
        >>> attach(clef, staff)
        ClefMark('alto')(Staff{4})
        >>> viola = instrumenttools.Viola()
        >>> attach(viola, staff)
        Viola()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "alto"
            \set Staff.instrumentName = \markup { Viola }
            \set Staff.shortInstrumentName = \markup { Va. }
            c'8
            d'8
            e'8
            f'8
        }

    The viola targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'viola'
        self._default_performer_names.extend([
            'string player',
            'violist',
            ])
        self._default_short_instrument_name = 'va.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [contexttools.ClefMark('alto')]
        self.allowable_clefs = [
            contexttools.ClefMark('alto'),
            contexttools.ClefMark('treble')]
        self._default_pitch_range = pitchtools.PitchRange(-12, 28)
