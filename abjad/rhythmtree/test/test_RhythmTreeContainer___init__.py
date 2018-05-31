import abjad
from abjad import rhythmtree


def test_RhythmTreeContainer___init___01():

    container = rhythmtree.RhythmTreeContainer()

    assert container.children == ()
    assert container.preprolated_duration == 1
    assert container.start_offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___02():

    container = rhythmtree.RhythmTreeContainer(
        preprolated_duration=2, children=[])

    assert container.children == ()
    assert container.preprolated_duration == 2
    assert container.start_offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___03():

    leaf_a = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)
    leaf_b = rhythmtree.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = rhythmtree.RhythmTreeLeaf(preprolated_duration=1)

    assert leaf_a.start_offset == 0
    assert leaf_a.parent is None

    assert leaf_b.start_offset == 0
    assert leaf_b.parent is None

    assert leaf_c.start_offset == 0
    assert leaf_c.parent is None

    container = rhythmtree.RhythmTreeContainer(
        preprolated_duration=4, children=[leaf_a, leaf_b, leaf_c])

    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert container.preprolated_duration == 4
    assert container.start_offset == 0
    assert container.parent is None

    assert leaf_a.start_offset == 0
    assert leaf_a.parent is container

    assert leaf_b.start_offset == 1
    assert leaf_b.parent is container

    assert leaf_c.start_offset == 3
    assert leaf_c.parent is container
