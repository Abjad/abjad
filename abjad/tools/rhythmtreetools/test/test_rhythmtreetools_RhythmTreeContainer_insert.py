# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer_insert_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)

    container = rhythmtreetools.RhythmTreeContainer()
    assert container.children == ()

    container.insert(0, leaf_a)
    assert container.children == (leaf_a,)

    container.insert(0, leaf_b)
    assert container.children == (leaf_b, leaf_a)

    container.insert(1, leaf_c)
    assert container.children == (leaf_b, leaf_c, leaf_a)
