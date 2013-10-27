# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_TimeIntervalTree_latest_stop_01():
    r'''latest_stop returns maximum stop_offset value of all intervals in tree.
    '''
    blocks = timeintervaltools.make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = TimeIntervalTree(blocks)
        assert tree.latest_stop == 37

def test_timeintervaltools_TimeIntervalTree_latest_stop_02():
    r'''latest_stop returns None if no intervals in tree.
    '''
    tree = TimeIntervalTree([])
    assert tree.latest_stop is None
