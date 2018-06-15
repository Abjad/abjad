import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer_insert_01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)

    container = abjad.rhythmtrees.RhythmTreeContainer()
    assert container.children == ()

    container.insert(0, leaf_a)
    assert container.children == (leaf_a,)

    container.insert(0, leaf_b)
    assert container.children == (leaf_b, leaf_a)

    container.insert(1, leaf_c)
    assert container.children == (leaf_b, leaf_c, leaf_a)
