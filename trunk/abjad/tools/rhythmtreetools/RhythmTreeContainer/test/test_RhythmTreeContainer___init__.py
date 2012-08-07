from abjad import *


def test_RhythmTreeContainer___init___01():

    container = rhythmtreetools.RhythmTreeContainer()

    assert container.children == ()
    assert container.duration == 1
    assert container.offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___02():

    container = rhythmtreetools.RhythmTreeContainer(2, [])

    assert container.children == ()
    assert container.duration == 2
    assert container.offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___03():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(1)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(1)

    assert leaf_a.offset == 0
    assert leaf_a.parent is None

    assert leaf_b.offset == 0
    assert leaf_b.parent is None

    assert leaf_c.offset == 0
    assert leaf_c.parent is None

    container = rhythmtreetools.RhythmTreeContainer(4, [leaf_a, leaf_b, leaf_c])

    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert container.duration == 4
    assert container.offset == 0
    assert container.parent is None

    assert leaf_a.offset == 0
    assert leaf_a.parent is container

    assert leaf_b.offset == 1
    assert leaf_b.parent is container

    assert leaf_c.offset == 3
    assert leaf_c.parent is container
