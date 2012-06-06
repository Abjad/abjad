from abjad.tools.markuptools.Markup import Markup
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class MarkupInventory(ObjectInventory):
    '''.. versionadded:: 2.8

    Abjad model of an ordered list of markup::

        >>> inventory = markuptools.MarkupInventory(['foo', 'bar'])

    ::

        >>> inventory
        MarkupInventory([Markup(('foo',)), Markup(('bar',))])

    Markup inventories implement the list interface and are mutable.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ##

    @property
    def _item_callable(self):
        return Markup

    #@property
    #def _one_line_menuin_summary(self):
    #    return ', '.join([markup.markup_name for markup in self])
