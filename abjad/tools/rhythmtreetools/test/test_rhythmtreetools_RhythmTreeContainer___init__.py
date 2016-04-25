# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer___init___01():

    container = rhythmtreetools.RhythmTreeContainer()

    assert container.children == ()
    assert container.preprolated_duration == 1
    assert container.start_offset == 0
    assert container.parent is None


def test_rhythmtreetools_RhythmTreeContainer___init___02():

    container = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=2, children=[])

    assert container.children == ()
    assert container.preprolated_duration == 2
    assert container.start_offset == 0
    assert container.parent is None


def test_rhythmtreetools_RhythmTreeContainer___init___03():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)

    assert leaf_a.start_offset == 0
    assert leaf_a.parent is None

    assert leaf_b.start_offset == 0
    assert leaf_b.parent is None

    assert leaf_c.start_offset == 0
    assert leaf_c.parent is None

    container = rhythmtreetools.RhythmTreeContainer(
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
