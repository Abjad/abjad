from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_timeintervaltools_compute_depth_of_intervals_in_interval_01():
    a = TimeInterval(0, 3)
    b = TimeInterval(6, 12)
    c = TimeInterval(9, 15)
    tree = TimeIntervalTree([a, b, c])
    d = TimeInterval(1, 14)
    depth = compute_depth_of_intervals_in_interval(tree, d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((1, 3), 1), ((3, 6), 0), ((6, 9), 1),
        ((9, 12), 2), ((12, 14), 1)]

def test_timeintervaltools_compute_depth_of_intervals_in_interval_02():
    a = TimeInterval(0, 3)
    b = TimeInterval(6, 12)
    c = TimeInterval(9, 15)
    tree = TimeIntervalTree([a, b, c])
    d = TimeInterval(-1, 16)
    depth = compute_depth_of_intervals_in_interval(tree, d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((-1, 0), 0), ((0, 3), 1), ((3, 6), 0), ((6, 9), 1),
        ((9, 12), 2), ((12, 15), 1), ((15, 16), 0)]

def test_timeintervaltools_compute_depth_of_intervals_in_interval_03():
    a = TimeInterval(0, 3)
    b = TimeInterval(6, 12)
    c = TimeInterval(9, 15)
    tree = TimeIntervalTree([a, b, c])
    d = TimeInterval(2001, 2010)
    depth = compute_depth_of_intervals_in_interval(tree, d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((2001, 2010), 0)]
