# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class TempoInventory(TypedList):
    r'''An ordered list of tempo indications.

    ::

        >>> inventory = indicatortools.TempoInventory([
        ...     ('Andante', Duration(1, 8), 72),
        ...     ('Allegro', Duration(1, 8), 84),
        ...     ])

    ::

        >>> for tempo in inventory:
        ...     tempo
        ...
        Tempo('Andante', Duration(1, 8), 72)
        Tempo('Allegro', Duration(1, 8), 84)

    Tempo inventories implement list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        from abjad.tools import indicatortools
        return indicatortools.Tempo
