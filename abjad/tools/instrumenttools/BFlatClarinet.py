# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BFlatClarinet(Instrument):
    r'''A B-flat clarinet.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = instrumenttools.BFlatClarinet()
        >>> attach(clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'cl.'

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='clarinet in B-flat',
        short_instrument_name='cl. in B-flat',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[D3, Bb6]',
        sounding_pitch_of_written_middle_c='Bb3',
        ):
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._is_primary_instrument = True

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

        Returns list.
        '''
        return super(BFlatClarinet, self)._get_performer_names()
