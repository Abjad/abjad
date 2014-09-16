# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TypedList


class SelectionInventory(TypedList):
    r'''An inventory of component selections.

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
        return selectiontools.SliceSelection