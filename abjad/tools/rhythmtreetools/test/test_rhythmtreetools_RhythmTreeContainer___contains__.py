# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer___contains___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)

    subcontainer = rhythmtreetools.RhythmTreeContainer(preprolated_duration=1, children=[leaf_b])

    container = rhythmtreetools.RhythmTreeContainer(preprolated_duration=1, children=[leaf_a, subcontainer])

    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container
