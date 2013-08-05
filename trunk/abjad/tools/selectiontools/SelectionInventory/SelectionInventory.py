# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import ObjectInventory


class SelectionInventory(ObjectInventory):
    r'''An inventory of component selections:

    ::

        >>> inventory = selectiontools.SelectionInventory()

    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        from abjad.tools import selectiontools
        return selectiontools.SliceSelection
