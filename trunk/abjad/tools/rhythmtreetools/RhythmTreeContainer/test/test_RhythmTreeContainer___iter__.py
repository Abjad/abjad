from abjad import *


def test_RhythmTreeContainer___iter___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(duration=2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(duration=1)

    container = rhythmtreetools.RhythmTreeContainer(
        duration=1, children=[leaf_a, leaf_b, leaf_c])

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
