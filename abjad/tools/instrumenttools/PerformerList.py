# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class PerformerList(TypedList):
    r'''Performer list.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def get_instrument(self, instrument_name):
        r'''Gets first instrument in performer list with `instrument_name`.

        ..  container:: example

            ::
            
                >>> flutist = instrumenttools.Performer(name='flutist')
                >>> flutist.instruments.append(instrumenttools.Flute())
                >>> flutist.instruments.append(instrumenttools.Piccolo())
                >>> performers = instrumenttools.PerformerList(
                ...     [flutist],
                ...     )
                >>> performers.get_instrument('piccolo')
                Piccolo()

        Returns instrument or none.
        '''
        for performer in self:
            instrument = performer.get_instrument(instrument_name)
            if instrument is not None:
                return instrument
