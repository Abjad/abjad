# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BFlatClarinet(Instrument):
    r'''A B-flat clarinet.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> clarinet = instrumenttools.BFlatClarinet()(staff)
        >>> clarinet
        BFlatClarinet()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The B-flat clarinet targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'clarinet in B-flat'
        self.default_performer_abbreviation = 'cl.'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._default_short_instrument_name = 'cl. in B-flat'
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('bf')
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._default_pitch_range = pitchtools.PitchRange(-10, 34)
        self._is_primary_instrument = True
        self._copy_default_starting_clefs_to_default_allowable_clefs()

    ### PUBLIC METHODS ###

    def _get_performer_names(self):
        r'''Get performer names:

        ::

            >>> for performer_name in clarinet._get_performer_names():
            ...     performer_name
            'instrumentalist'
            'wind player'
            'reed player'
            'single reed player'
            'clarinettist'
            'clarinetist'

        Return list.
        '''
        return super(BFlatClarinet, self)._get_performer_names()
