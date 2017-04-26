# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TypedList


class SelectionList(TypedList):
    r'''Selection list.

    ..  container:: example

        ::

            >>> selections = selectiontools.SelectionList()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import selectiontools
        return selectiontools.Selection
