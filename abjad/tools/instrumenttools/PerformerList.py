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
            
                >>> flutist = abjad.instrumenttools.Performer(name='flutist')
                >>> flutist.instruments.append(abjad.instrumenttools.Flute())
                >>> flutist.instruments.append(abjad.instrumenttools.Piccolo())
                >>> performers = abjad.instrumenttools.PerformerList(
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
