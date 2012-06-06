from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from abjad.tools.pitchtools.PitchRange import PitchRange


class PitchRangeInventory(ObjectInventory):
    r'''.. versionadded:: 2.7

    Abjad model of an ordered list of pitch ranges::

        >>> pitchtools.PitchRangeInventory(['[C3, C6]', '[C4, C6]'])
        PitchRangeInventory([PitchRange('[C3, C6]'), PitchRange('[C4, C6]')])

    Pitch range inventories implement list interface and are mutable.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property   
    def _item_callable(self):
        return PitchRange
