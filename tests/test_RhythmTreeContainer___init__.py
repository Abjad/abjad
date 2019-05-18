import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer___init___01():

    container = abjad.rhythmtrees.RhythmTreeContainer()

    assert container.children == ()
    assert container.preprolated_duration == 1
    assert container.start_offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___02():

    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2, children=[]
    )

    assert container.children == ()
    assert container.preprolated_duration == 2
    assert container.start_offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___03():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)

    assert leaf_a.start_offset == 0
    assert leaf_a.parent is None

    assert leaf_b.start_offset == 0
    assert leaf_b.parent is None

    assert leaf_c.start_offset == 0
    assert leaf_c.parent is None

    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=4, children=[leaf_a, leaf_b, leaf_c]
    )

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
