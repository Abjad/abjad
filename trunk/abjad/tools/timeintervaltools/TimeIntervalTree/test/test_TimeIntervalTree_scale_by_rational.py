# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_scale_by_rational_01():
    t1 = timeintervaltools.TimeInterval(0, 4)
    t2 = timeintervaltools.TimeInterval(2, 6)
    t3 = timeintervaltools.TimeInterval(1, 8)

    tree = timeintervaltools.TimeIntervalTree([t1, t2, t3])
    scalar = durationtools.Multiplier(1, 2)
    result = tree.scale_by_rational(scalar)

    assert type(result) == type(tree)
    assert [x.signature for x in result] == [
        (Offset(0, 1), Offset(2, 1)),
        (Offset(1, 2), Offset(4, 1)),
        (Offset(1, 1), Offset(3, 1))]
    assert result.duration == tree.duration * scalar
    for old, new in zip(tree, result):
        assert new.duration == old.duration * scalar


def test_TimeIntervalTree_scale_by_rational_02():
    t0 = timeintervaltools.TimeInterval(-3, -1)
    t1 = timeintervaltools.TimeInterval(0, 4)
    t2 = timeintervaltools.TimeInterval(2, 6)
    t3 = timeintervaltools.TimeInterval(1, 8)

    tree = timeintervaltools.TimeIntervalTree([t0, t1, t2, t3])
    scalar = durationtools.Multiplier(1, 2)
    result = tree.scale_by_rational(scalar)

    assert type(result) == type(tree)
    assert [x.signature for x in result] == [
        (Offset(-3, 1), Offset(-2, 1)),
        (Offset(-3, 2), Offset(1, 2)),
        (Offset(-1, 1), Offset(5, 2)),
        (Offset(-1, 2), Offset(3, 2))]
    assert result.duration == tree.duration * scalar
    for old, new in zip(tree, result):
        assert new.duration == old.duration * scalar


def test_TimeIntervalTree_scale_by_rational_03():
    a = timeintervaltools.TimeInterval(durationtools.Multiplier(-1, 2), 1)
    b = timeintervaltools.TimeInterval(2, durationtools.Multiplier(7, 3))
    tree = timeintervaltools.TimeIntervalTree([a, b])
    rational = 2
    result = tree.scale_by_rational(rational)
    assert result.duration == tree.duration * rational
    assert [x.signature for x in result] == \
        [(Offset(-1, 2), Offset(5, 2)), 
        (Offset(9, 2), Offset(31, 6))]


def test_TimeIntervalTree_scale_by_rational_04():
    a = timeintervaltools.TimeInterval(durationtools.Multiplier(-1, 2), 1)
    b = timeintervaltools.TimeInterval(2, durationtools.Multiplier(7, 3))
    tree = timeintervaltools.TimeIntervalTree([a, b])
    rational = -1
    py.test.raises(AssertionError,
        "result = tree.scale_by_rational(rational)")


def test_TimeIntervalTree_scale_by_rational_05():
    a = timeintervaltools.TimeInterval(durationtools.Multiplier(-1, 2), 1)
    b = timeintervaltools.TimeInterval(2, durationtools.Multiplier(7, 3))
    tree = timeintervaltools.TimeIntervalTree([a, b])
    rational = 0
    py.test.raises(AssertionError,
        "result = tree.scale_by_rational(rational)")
