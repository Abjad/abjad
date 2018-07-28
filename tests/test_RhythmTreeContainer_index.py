import abjad
import pytest
import abjad.rhythmtrees


def test_RhythmTreeContainer_index_01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2, children=[leaf_b, leaf_c])
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)
    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, subcontainer, leaf_d])

    assert container.index(leaf_a) == 0
    assert container.index(subcontainer) == 1
    assert container.index(leaf_d) == 2

    pytest.raises(ValueError, 'container.index(leaf_b)')
    pytest.raises(ValueError, 'container.index(leaf_c)')
