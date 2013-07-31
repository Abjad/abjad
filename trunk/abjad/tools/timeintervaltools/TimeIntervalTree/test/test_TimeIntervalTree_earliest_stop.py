# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree_earliest_stop_01():
    r'''earliest_stop returns minimum stop_offset value of all intervals in tree.
    '''
    blocks = timeintervaltools.make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = TimeIntervalTree(blocks)
        assert tree.earliest_stop == 3

def test_TimeIntervalTree_earliest_stop_02():
    r'''earliest_stop returns None if no intervals in tree.
    '''
    tree = TimeIntervalTree([])
    assert tree.earliest_stop is None
