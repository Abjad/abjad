# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_rhythmtreetools_RhythmTreeContainer___getitem___01():

    leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
    leaf_c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)

    container = rhythmtreetools.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, leaf_b, leaf_c])

    assert container[0] is leaf_a
    assert container[1] is leaf_b
    assert container[2] is leaf_c

    pytest.raises(Exception, 'container[3]')

    assert container[-1] is leaf_c
    assert container[-2] is leaf_b
    assert container[-3] is leaf_a

    pytest.raises(Exception, 'container[-4]')
