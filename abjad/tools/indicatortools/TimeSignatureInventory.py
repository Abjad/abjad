# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class TimeSignatureInventory(TypedList):
    '''An ordered list of time signatures.

    ::

        >>> inventory = indicatortools.TimeSignatureInventory([(5, 8), (4, 4)])

    ::

        >>> inventory
        TimeSignatureInventory([TimeSignature((5, 8)), TimeSignature((4, 4))])

    ::

        >>> (5, 8) in inventory
        True

    ::

        >>> TimeSignature((4, 4)) in inventory
        True

    ::

        >>> (3, 4) in inventory
        False

    ::

        >>> show(inventory) # doctest: +SKIP

    Time signature inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        from abjad.tools import indicatortools
        return indicatortools.TimeSignature

    @property
    def _one_line_menuing_summary(self):
        return ', '.join([time_signature.pair for time_signature in self])
