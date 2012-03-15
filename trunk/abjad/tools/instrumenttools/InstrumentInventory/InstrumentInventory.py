from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class InstrumentInventory(ObjectInventory):
    r'''.. versionadded:: 2.8

    Abjad model of an ordered list of instruments::

        abjad> inventory = instrumenttools.InstrumentInventory([instrumenttools.Flute(), instrumenttools.Guitar()])

    ::

        abjad> inventory
        InstrumentInventory([Flute(), Guitar()])

    Instrument inventories implement list interface and are mutable.
    '''

    ### PRIVATE READ-ONLY PROPERTIES ###

    # TODO: possibly abstract up to ObjectInventory as default
    @property
    def _item_class(self):
        return lambda x: x
