from abjad import *


def test_RhythmTreeContainer___contains___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(1)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(1)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(1)

    subcontainer = rhythmtreetools.RhythmTreeContainer(1, [leaf_b])

    container = rhythmtreetools.RhythmTreeContainer(1, [leaf_a, subcontainer])

    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container
