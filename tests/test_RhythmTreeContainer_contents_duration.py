import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer_contents_duration_01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2, children=[leaf_b, leaf_c])
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)

    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, subcontainer, leaf_d])

    assert container._get_contents_duration() == 6
    assert subcontainer._get_contents_duration() == 5
