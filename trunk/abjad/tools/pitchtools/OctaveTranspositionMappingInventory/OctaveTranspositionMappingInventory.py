from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from abjad.tools.pitchtools.OctaveTranspositionMapping import OctaveTranspositionMapping


class OctaveTranspositionMappingInventory(ObjectInventory):
    '''.. versionadded:: 2.8

    Model of an ordered list of octave transposition mappings::

        abjad> mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
        abjad> mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
        abjad> inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])

    ::

        abjad> inventory
        OctaveTranspositionMappingInventory([OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)]), OctaveTranspositionMapping([('[A0, C8]', -18)])])

    Octave transposition mapping inventories implement list interface and are mutable.
    '''

    ### PRIVATE READ-ONLY PROPERTIES ###
    
    @property
    def _item_callable(self):
        return OctaveTranspositionMapping
