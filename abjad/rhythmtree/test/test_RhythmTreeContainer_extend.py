import abjad
from abjad import rhythmtree


def test_RhythmTreeContainer_extend_01():

    leaf_a = rhythmtree.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtree.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = rhythmtree.RhythmTreeLeaf(preprolated_duration=2)
    leaf_d = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)

    container = rhythmtree.RhythmTreeContainer()

    assert container.children == ()

    container.extend([leaf_a])
    assert container.children == (leaf_a,)

    container.extend([leaf_b, leaf_c, leaf_d])
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)

    container.extend([leaf_a, leaf_c])
    assert container.children == (leaf_b, leaf_d, leaf_a, leaf_c)
