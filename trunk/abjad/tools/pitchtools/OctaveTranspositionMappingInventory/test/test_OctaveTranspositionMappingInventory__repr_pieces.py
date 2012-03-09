from abjad import *


def test_OctaveTranspositionMappingInventory__repr_pieces_01():

    inventory = pitchtools.OctaveTranspositionMappingInventory([
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', -24), 
            pitchtools.OctaveTranspositionMappingComponent('[C4, C8]', -17)]),
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', -19), 
            pitchtools.OctaveTranspositionMappingComponent('[C4, C8]', -12)]),
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', -12),
            pitchtools.OctaveTranspositionMappingComponent('[C4, C8]', -5)]),
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', -7), 
            pitchtools.OctaveTranspositionMappingComponent('[C4, C8]', 0)])])

    r'''
    OctaveTranspositionMappingInventory([
        OctaveTranspositionMapping([
            OctaveTranspositionMappingComponent('[A0, C4)', -24),
            OctaveTranspositionMappingComponent('[C4, C8]', -17)
        ]),
        OctaveTranspositionMapping([
            OctaveTranspositionMappingComponent('[A0, C4)', -19),
            OctaveTranspositionMappingComponent('[C4, C8]', -12)
        ]),
        OctaveTranspositionMapping([
            OctaveTranspositionMappingComponent('[A0, C4)', -12),
            OctaveTranspositionMappingComponent('[C4, C8]', -5)
        ]),
        OctaveTranspositionMapping([
            OctaveTranspositionMappingComponent('[A0, C4)', -7),
            OctaveTranspositionMappingComponent('[C4, C8]', 0)
        ])
    ])
    '''

    assert ''.join(inventory._repr_pieces) == "OctaveTranspositionMappingInventory([\tOctaveTranspositionMapping([\t\tOctaveTranspositionMappingComponent('[A0, C4)', -24),\t\tOctaveTranspositionMappingComponent('[C4, C8]', -17)\t]),\tOctaveTranspositionMapping([\t\tOctaveTranspositionMappingComponent('[A0, C4)', -19),\t\tOctaveTranspositionMappingComponent('[C4, C8]', -12)\t]),\tOctaveTranspositionMapping([\t\tOctaveTranspositionMappingComponent('[A0, C4)', -12),\t\tOctaveTranspositionMappingComponent('[C4, C8]', -5)\t]),\tOctaveTranspositionMapping([\t\tOctaveTranspositionMappingComponent('[A0, C4)', -7),\t\tOctaveTranspositionMappingComponent('[C4, C8]', 0)\t])])"
