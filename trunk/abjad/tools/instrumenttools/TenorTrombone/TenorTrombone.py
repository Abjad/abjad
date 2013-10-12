# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorTrombone(Instrument):
    r'''Abjad model of the tenor trombone:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        >>> instrumenttools.TenorTrombone()(staff)
        TenorTrombone()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tenor trombone }
            \set Staff.shortInstrumentName = \markup { Ten. trb. }
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
        self._default_instrument_name = 'tenor trombone'
        self.default_performer_abbreviation = 'trb.'
        self._default_performer_names.extend([
            'brass player',
            'trombonist',
            ])
        self._default_short_instrument_name = 'ten. trb.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [
            contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-20, 15)
        #self._make_default_name_markups()
