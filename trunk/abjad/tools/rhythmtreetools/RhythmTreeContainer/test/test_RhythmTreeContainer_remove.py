from abjad import *


def test_RhythmTreeContainer_remove_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(2)

    container = rhythmtreetools.RhythmTreeContainer(1, [leaf_a, leaf_b, leaf_c])
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert leaf_a.parent is container
    assert leaf_b.parent is container
    assert leaf_c.parent is container

    container.remove(leaf_a)
    assert container.children == (leaf_b, leaf_c)
    assert leaf_a.parent is None

    container.remove(leaf_c)
    assert container.children == (leaf_b,)
    assert leaf_c.parent is None
