from abjad.tools.contexttools.ClefMark import ClefMark
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class ClefMarkInventory(ObjectInventory):
    '''.. versionadded:: 2.8

    Abjad model of an ordered list of clefs::

        abjad> inventory = contexttools.ClefMarkInventory(['treble', 'bass'])

    ::

        abjad> inventory
        ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

    ::

        abjad> 'treble' in inventory
        True

    ::

        abjad> contexttools.ClefMark('treble') in inventory
        True

    ::

        abjad> 'alto' in inventory
        False

    Clef mark inventories implement list interface and are mutable.
    '''

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _item_class(self):
        return ClefMark
