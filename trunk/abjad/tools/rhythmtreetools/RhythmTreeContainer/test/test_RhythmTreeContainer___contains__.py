from abjad import *


def test_RhythmTreeContainer___contains___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(duration=1)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(duration=1)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(duration=1)

    subcontainer = rhythmtreetools.RhythmTreeContainer(duration=1, children=[leaf_b])

    container = rhythmtreetools.RhythmTreeContainer(duration=1, children=[leaf_a, subcontainer])

    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container
