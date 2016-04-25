# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer_append_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    leaf_d = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
    container = rhythmtreetools.RhythmTreeContainer()

    assert container.children == ()

    container.append(leaf_a)
    assert container.children == (leaf_a,)

    container.append(leaf_b)
    assert container.children == (leaf_a, leaf_b)

    container.append(leaf_c)
    assert container.children == (leaf_a, leaf_b, leaf_c)

    container.append(leaf_d)
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)

    container.append(leaf_a)
    assert container.children == (leaf_b, leaf_c, leaf_d, leaf_a)
