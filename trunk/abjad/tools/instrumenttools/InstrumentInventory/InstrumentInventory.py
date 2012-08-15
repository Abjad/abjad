from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class InstrumentInventory(ObjectInventory):
    r'''.. versionadded:: 2.8

    Abjad model of an ordered list of instruments::

        >>> inventory = instrumenttools.InstrumentInventory(
        ...     [instrumenttools.Flute(), instrumenttools.Guitar()])

    ::

        >>> inventory
        InstrumentInventory([Flute(), Guitar()])

    Instrument inventories implement list interface and are mutable.
    '''

    pass
