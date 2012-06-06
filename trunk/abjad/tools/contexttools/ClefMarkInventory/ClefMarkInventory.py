from abjad.tools.contexttools.ClefMark import ClefMark
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class ClefMarkInventory(ObjectInventory):
    '''.. versionadded:: 2.8

    Abjad model of an ordered list of clefs::

        >>> inventory = contexttools.ClefMarkInventory(['treble', 'bass'])

    ::

        >>> inventory
        ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

    ::

        >>> 'treble' in inventory
        True

    ::

        >>> contexttools.ClefMark('treble') in inventory
        True

    ::

        >>> 'alto' in inventory
        False

    Clef mark inventories implement list interface and are mutable.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return ClefMark

    @property
    def _one_line_menuing_summary(self):
        return ', '.join([clef_mark.clef_name for clef_mark in self])
