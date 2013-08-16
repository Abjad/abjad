# -*- encoding: utf-8 -*-
from abjad.tools.contexttools.TempoMark import TempoMark
from abjad.tools.datastructuretools.TypedList import TypedList


class TempoMarkInventory(TypedList):
    r'''Abjad model of an ordered list of tempo marks:

    ::

        >>> inventory = contexttools.TempoMarkInventory([
        ...     ('Andante', Duration(1, 8), 72),
        ...     ('Allegro', Duration(1, 8), 84)])

    ::

        >>> for tempo_mark in inventory:
        ...     tempo_mark
        ...
        TempoMark('Andante', Duration(1, 8), 72)
        TempoMark('Allegro', Duration(1, 8), 84)

    Tempo mark inventories implement list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return TempoMark
