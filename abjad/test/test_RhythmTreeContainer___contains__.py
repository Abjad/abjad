import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer___contains___01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)

    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(preprolated_duration=1, children=[leaf_b])

    container = abjad.rhythmtrees.RhythmTreeContainer(preprolated_duration=1, children=[leaf_a, subcontainer])

    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container
