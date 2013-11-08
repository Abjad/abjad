# -*- encoding: utf-8 -*-
from abjad.tools.marktools.Tempo import Tempo
from abjad.tools.datastructuretools.TypedList import TypedList


class TempoInventory(TypedList):
    r'''An ordered list of tempo marks.

    ::

        >>> inventory = marktools.TempoInventory([
        ...     ('Andante', Duration(1, 8), 72),
        ...     ('Allegro', Duration(1, 8), 84)])

    ::

        >>> for tempo_mark in inventory:
        ...     tempo_mark
        ...
        Tempo('Andante', Duration(1, 8), 72)
        Tempo('Allegro', Duration(1, 8), 84)

    Tempo mark inventories implement list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Tempo
