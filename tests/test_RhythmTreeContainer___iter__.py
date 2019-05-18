import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer___iter___01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)

    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, leaf_b, leaf_c]
    )

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
