from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_compute_depth_of_intervals_in_interval_01():
    a = BoundedInterval(0, 3)
    b = BoundedInterval(6, 12)
    c = BoundedInterval(9, 15)
    tree = IntervalTree([a, b, c])
    d = BoundedInterval(1, 14)
    depth = compute_depth_of_intervals_in_interval(tree, d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((1, 3), 1), ((3, 6), 0), ((6, 9), 1),
        ((9, 12), 2), ((12, 14), 1)]

def test_intervaltreetools_compute_depth_of_intervals_in_interval_02():
    a = BoundedInterval(0, 3)
    b = BoundedInterval(6, 12)
    c = BoundedInterval(9, 15)
    tree = IntervalTree([a, b, c])
    d = BoundedInterval(-1, 16)
    depth = compute_depth_of_intervals_in_interval(tree, d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((-1, 0), 0), ((0, 3), 1), ((3, 6), 0), ((6, 9), 1),
        ((9, 12), 2), ((12, 15), 1), ((15, 16), 0)]

def test_intervaltreetools_compute_depth_of_intervals_in_interval_03():
    a = BoundedInterval(0, 3)
    b = BoundedInterval(6, 12)
    c = BoundedInterval(9, 15)
    tree = IntervalTree([a, b, c])
    d = BoundedInterval(2001, 2010)
    depth = compute_depth_of_intervals_in_interval(tree, d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((2001, 2010), 0)]
