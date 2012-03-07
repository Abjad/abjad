from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree___iter____01():
    blocks = _make_test_intervals()
    tree = TimeIntervalTree(blocks)
    for e in enumerate(tree):
        assert blocks[e[0]] == e[1]
