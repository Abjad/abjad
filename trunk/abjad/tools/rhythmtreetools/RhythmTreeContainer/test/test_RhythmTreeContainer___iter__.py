from abjad import *


def test_RhythmTreeContainer___iter___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(1)

    container = rhythmtreetools.RhythmTreeContainer(1, [leaf_a, leaf_b, leaf_c])

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
