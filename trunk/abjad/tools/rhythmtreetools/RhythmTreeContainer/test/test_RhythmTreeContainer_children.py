from abjad import *


def test_RhythmTreeContainer_children_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(2)
    subcontainer = rhythmtreetools.RhythmTreeContainer(2, [leaf_b, leaf_c])
    leaf_d = rhythmtreetools.RhythmTreeLeaf(1)

    container = rhythmtreetools.RhythmTreeContainer(1, [leaf_a, subcontainer, leaf_d])
    
    assert container.children == (leaf_a, subcontainer, leaf_d)
