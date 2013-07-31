# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeIntervalTree_compute_depth_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    depths = tree.compute_depth()
    target = [
        ((0, 3), 1),
        ((3, 5), 0),
        ((5, 6), 1),
        ((6, 8), 2),
        ((8, 9), 3),
        ((9, 10), 2),
        ((10, 13), 1),
        ((13, 15), 0),
        ((15, 16), 1),
        ((16, 17), 2),
        ((17, 19), 3),
        ((19, 20), 3),
        ((20, 21), 2),
        ((21, 23), 1),
        ((23, 25), 0),
        ((25, 26), 1),
        ((26, 29), 2),
        ((29, 30), 1),
        ((30, 32), 0),
        ((32, 34), 1),
        ((34, 37), 1),
    ]
    actual = [(i.signature, i['depth']) for i in depths]
    assert actual == target


def test_TimeIntervalTree_compute_depth_02():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(1, 14)
    depth = tree.compute_depth(bounding_interval=d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((1, 3), 1), ((3, 6), 0), ((6, 9), 1),
        ((9, 12), 2), ((12, 14), 1)]


def test_TimeIntervalTree_compute_depth_03():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(-1, 16)
    depth = tree.compute_depth(bounding_interval=d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((-1, 0), 0), ((0, 3), 1), ((3, 6), 0), ((6, 9), 1),
        ((9, 12), 2), ((12, 15), 1), ((15, 16), 0)]


def test_TimeIntervalTree_compute_depth_04():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(2001, 2010)
    depth = tree.compute_depth(bounding_interval=d)
    assert [(x.signature, x['depth']) for x in depth] == \
        [((2001, 2010), 0)]
