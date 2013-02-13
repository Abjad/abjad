from abjad import *
import py.test


def test_RhythmTreeContainer_index_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    subcontainer = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=2, children=[leaf_b, leaf_c])
    leaf_d = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
    container = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, subcontainer, leaf_d])

    assert container.index(leaf_a) == 0
    assert container.index(subcontainer) == 1
    assert container.index(leaf_d) == 2

    py.test.raises(ValueError, 'container.index(leaf_b)')
    py.test.raises(ValueError, 'container.index(leaf_c)')
