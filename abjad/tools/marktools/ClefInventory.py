# -*- encoding: utf-8 -*-
from abjad.tools.marktools.Clef import Clef
from abjad.tools.datastructuretools.TypedList import TypedList


class ClefInventory(TypedList):
    '''An ordered list of clefs.

    ::

        >>> inventory = marktools.ClefInventory(['treble', 'bass'])

    ::

        >>> inventory
        ClefInventory([Clef('treble'), Clef('bass')])

    ::

        >>> 'treble' in inventory
        True

    ::

        >>> marktools.Clef('treble') in inventory
        True

    ::

        >>> 'alto' in inventory
        False

    Clef mark inventories implement list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Clef

    @property
    def _one_line_menuing_summary(self):
        return ', '.join([clef_mark.clef_name for clef_mark in self])
