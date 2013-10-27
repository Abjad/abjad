# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.pitchtools.PitchRange import PitchRange


class PitchRangeInventory(TypedList):
    r'''An ordered list of pitch ranges.

    ::

        >>> pitchtools.PitchRangeInventory(['[C3, C6]', '[C4, C6]'])
        PitchRangeInventory([PitchRange('[C3, C6]'), PitchRange('[C4, C6]')])

    Pitch range inventories implement list interface and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return PitchRange
