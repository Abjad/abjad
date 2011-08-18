from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree___contains____01():
    blocks = _make_test_intervals()
    tree = IntervalTree(blocks[0])
    assert blocks[0] in tree

def test_IntervalTree___contains____02():
    blocks = _make_test_intervals()
    tree = IntervalTree(blocks[0])
    assert blocks[1] not in tree
