from abjad import *


def test_RhythmTreeContainer_extend_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(2)
    leaf_d = rhythmtreetools.RhythmTreeLeaf(1)

    container = rhythmtreetools.RhythmTreeContainer()

    assert container.children == ()

    container.extend([leaf_a])
    assert container.children == (leaf_a,)

    container.extend([leaf_b, leaf_c, leaf_d])
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)

    container.extend([leaf_a, leaf_c])
    assert container.children == (leaf_b, leaf_d, leaf_a, leaf_c)
