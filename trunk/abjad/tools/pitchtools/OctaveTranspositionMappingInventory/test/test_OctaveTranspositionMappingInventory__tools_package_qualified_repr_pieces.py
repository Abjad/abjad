from abjad import *


def test_OctaveTranspositionMappingInventory__tools_package_qualified_repr_pieces_01():

    mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
    inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])

    r'''
    pitchtools.OctaveTranspositionMappingInventory([
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', 15),
            pitchtools.OctaveTranspositionMappingComponent('[C4, C8)', 27)
        ]),
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)
        ])
    ])
    '''

    assert '\n'.join(inventory._tools_package_qualified_repr_pieces) == "pitchtools.OctaveTranspositionMappingInventory([\n\tpitchtools.OctaveTranspositionMapping([\n\t\tpitchtools.OctaveTranspositionMappingComponent('[A0, C4)', 15),\n\t\tpitchtools.OctaveTranspositionMappingComponent('[C4, C8)', 27)\n\t]),\n\tpitchtools.OctaveTranspositionMapping([\n\t\tpitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)\n\t])\n])"
