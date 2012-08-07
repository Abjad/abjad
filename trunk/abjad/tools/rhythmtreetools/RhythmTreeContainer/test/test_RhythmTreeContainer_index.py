from abjad import *
import py.test


def test_RhythmTreeContainer_index_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(2)
    subcontainer = rhythmtreetools.RhythmTreeContainer(2, [leaf_b, leaf_c])
    leaf_d = rhythmtreetools.RhythmTreeLeaf(1)
    container = rhythmtreetools.RhythmTreeContainer(1, [leaf_a, subcontainer, leaf_d])

    assert container.index(leaf_a) == 0
    assert container.index(subcontainer) == 1
    assert container.index(leaf_d) == 2

    py.test.raises(ValueError, 'container.index(leaf_b)')
    py.test.raises(ValueError, 'container.index(leaf_c)')
