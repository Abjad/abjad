# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TypedList


class SelectionInventory(TypedList):
    r'''A selection inventory.

    ::

        >>> inventory = selectiontools.SelectionInventory()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import selectiontools
        return selectiontools.Selection
