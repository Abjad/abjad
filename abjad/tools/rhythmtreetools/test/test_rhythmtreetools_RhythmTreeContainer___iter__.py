# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer___iter___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)

    container = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, leaf_b, leaf_c])

    assert [x for x in container] == [leaf_a, leaf_b, leaf_c]
