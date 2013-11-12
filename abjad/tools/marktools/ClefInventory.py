# -*- encoding: utf-8 -*-
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

        >>> Clef('treble') in inventory
        True

    ::

        >>> 'alto' in inventory
        False

    Clef inventories implement list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        from abjad.tools import marktools
        return marktools.Clef

    @property
    def _one_line_menuing_summary(self):
        return ', '.join([clef.name for clef in self])
