# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class InstrumentInventory(TypedList):
    r'''Abjad model of an ordered list of instruments:

    ::

        >>> inventory = instrumenttools.InstrumentInventory(
        ...     [instrumenttools.Flute(), instrumenttools.Guitar()])

    ::

        >>> inventory
        InstrumentInventory([Flute(), Guitar()])

    Instrument inventories implement list interface and are mutable.
    '''

    pass
