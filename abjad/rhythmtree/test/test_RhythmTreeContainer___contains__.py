import abjad
from abjad import rhythmtree


def test_RhythmTreeContainer___contains___01():

    leaf_a = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)
    leaf_b = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)
    leaf_c = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)

    subcontainer = rhythmtree.RhythmTreeContainer(preprolated_duration=1, children=[leaf_b])

    container = rhythmtree.RhythmTreeContainer(preprolated_duration=1, children=[leaf_a, subcontainer])

    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container
