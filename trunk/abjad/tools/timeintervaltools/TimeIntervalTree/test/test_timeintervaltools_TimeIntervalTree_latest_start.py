# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_TimeIntervalTree_latest_start_01():
    r'''latest_start returns maximum start_offset value of all intervals in tree.
    '''
    blocks = timeintervaltools.make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = TimeIntervalTree(blocks)
        assert tree.latest_start == 34

def test_timeintervaltools_TimeIntervalTree_latest_start_02():
    r'''latest_start returns None if no intervals in tree.
    '''
    tree = TimeIntervalTree([])
    assert tree.latest_start is None
