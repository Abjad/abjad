# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer_rtm_format_01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    subcontainer = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=2, children=[leaf_b, leaf_c])
    leaf_d = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
    container = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, subcontainer, leaf_d])

    assert subcontainer.rtm_format == '(2 (3 2))'
    assert container.rtm_format == '(1 (3 (2 (3 2)) 1))'
