from abjad.tools.contexttools.TempoMark import TempoMark
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TempoMarkInventory(ObjectInventory):
    r'''.. versionadded:: 2.7

    Abjad model of an ordered list of tempo marks::

        abjad> contexttools.TempoMarkInventory([('Andante', Duration(1, 8), 72), ('Allegro', Duration(1, 8), 84)])
        TempoMarkInventory([TempoMark('Andante', Duration(1, 8), 72), TempoMark('Allegro', Duration(1, 8), 84)])

    Tempo mark inventories implement list interface and are mutable.
    '''

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _item_callable(self):
        return TempoMark
