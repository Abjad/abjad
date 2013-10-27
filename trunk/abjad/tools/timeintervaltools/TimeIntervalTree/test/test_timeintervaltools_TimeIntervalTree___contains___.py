# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_TimeIntervalTree___contains____01():
    blocks = timeintervaltools.make_test_intervals()
    tree = TimeIntervalTree(blocks[0])
    assert blocks[0] in tree

def test_timeintervaltools_TimeIntervalTree___contains____02():
    blocks = timeintervaltools.make_test_intervals()
    tree = TimeIntervalTree(blocks[0])
    assert blocks[1] not in tree
