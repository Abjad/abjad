# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.markuptools.Markup import Markup


class MarkupInventory(TypedList):
    '''Abjad model of an ordered list of markup:

    ::

        >>> inventory = markuptools.MarkupInventory(['foo', 'bar'])

    ::

        >>> inventory
        MarkupInventory([Markup(contents=('foo',)), Markup(contents=('bar',))])

    Markup inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Markup
