# -*- encoding: utf-8 -*-
from abjad.tools.markuptools.Markup import Markup
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class MarkupInventory(ObjectInventory):
    '''Abjad model of an ordered list of markup:

    ::

        >>> inventory = markuptools.MarkupInventory(['foo', 'bar'])

    ::

        >>> inventory
        MarkupInventory([Markup(('foo',)), Markup(('bar',))])

    Markup inventories implement the list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Markup
