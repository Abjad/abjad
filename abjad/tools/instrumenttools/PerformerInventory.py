# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class PerformerInventory(TypedList):
    r'''Abjad model of an ordered list of performers.

    Performer inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def get_instrument(self, instrument_name):
        r'''Gets first instrument in performer inventory with
        `instrument_name`.

        ..  container:: example

            ::
            
                >>> flutist = instrumenttools.Performer(name='flutist')
                >>> flutist.instruments.append(instrumenttools.Flute())
                >>> flutist.instruments.append(instrumenttools.Piccolo())
                >>> inventory = instrumenttools.PerformerInventory(
                ...     [flutist],
                ...     )
                >>> inventory.get_instrument('piccolo')
                Piccolo()

        Returns instrument or none.
        '''
        for performer in self:
            instrument = performer.get_instrument(instrument_name)
            if instrument is not None:
                return instrument
