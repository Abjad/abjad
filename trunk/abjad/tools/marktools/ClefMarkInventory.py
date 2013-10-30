# -*- encoding: utf-8 -*-
from abjad.tools.marktools.ClefMark import ClefMark
from abjad.tools.datastructuretools.TypedList import TypedList


class ClefMarkInventory(TypedList):
    '''An ordered list of clefs.

    ::

        >>> inventory = marktools.ClefMarkInventory(['treble', 'bass'])

    ::

        >>> inventory
        ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

    ::

        >>> 'treble' in inventory
        True

    ::

        >>> marktools.ClefMark('treble') in inventory
        True

    ::

        >>> 'alto' in inventory
        False

    Clef mark inventories implement list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return ClefMark

    @property
    def _one_line_menuing_summary(self):
        return ', '.join([clef_mark.clef_name for clef_mark in self])
