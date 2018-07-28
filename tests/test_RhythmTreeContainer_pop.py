import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer_pop_01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)

    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, leaf_b, leaf_c])
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert leaf_a.parent is container
    assert leaf_b.parent is container
    assert leaf_c.parent is container

    result = container.pop()
    assert container.children == (leaf_a, leaf_b)
    assert result is leaf_c
    assert result.parent is None

    result = container.pop(0)
    assert container.children == (leaf_b,)
    assert result is leaf_a
    assert result.parent is None
