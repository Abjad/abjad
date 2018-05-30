import abjad
from abjad import rhythmtree


def test_RhythmTreeContainer___iter___01():

    leaf_a = rhythmtree.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtree.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)

    container = rhythmtree.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, leaf_b, leaf_c])

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
