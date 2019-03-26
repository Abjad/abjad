import pytest
import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer___getitem___01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)

    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, leaf_b, leaf_c])

    assert container[0] is leaf_a
    assert container[1] is leaf_b
    assert container[2] is leaf_c

    with pytest.raises(Exception):
        container[3]

    assert container[-1] is leaf_c
    assert container[-2] is leaf_b
    assert container[-3] is leaf_a

    with pytest.raises(Exception):
        container[-4]
