from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree___contains____01():
    blocks = _make_test_intervals()
    tree = TimeIntervalTree(blocks[0])
    assert blocks[0] in tree

def test_TimeIntervalTree___contains____02():
    blocks = _make_test_intervals()
    tree = TimeIntervalTree(blocks[0])
    assert blocks[1] not in tree
