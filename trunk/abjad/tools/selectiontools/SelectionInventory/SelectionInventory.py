from abjad.tools.datastructuretools import ObjectInventory


class SelectionInventory(ObjectInventory):
    '''An inventory of component selections:

    ::

        >>> inventory = selectiontools.SelectionInventory()

    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        from abjad.tools import selectiontools
        return selectiontools.SequentialSelection
