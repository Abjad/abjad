from abjad import *
import py.test


def test_TimeIntervalTree_scale_to_rational_01():
    t1 = timeintervaltools.TimeInterval(0, 4)
    t2 = timeintervaltools.TimeInterval(1, 8)
    t3 = timeintervaltools.TimeInterval(2, 6)

    tree = timeintervaltools.TimeIntervalTree([t1, t2, t3])
    scalar = durationtools.Duration(1, 4)
    result = tree.scale_to_rational(scalar)

    assert type(result) == type(tree)
    assert [x.signature for x in result] == [
        (Offset(0, 1), Offset(1, 8)),
        (Offset(1, 32), Offset(1, 4)),
        (Offset(1, 16), Offset(3, 16))]
    assert result.duration == scalar


def test_TimeIntervalTree_scale_to_rational_02():
    a = timeintervaltools.TimeInterval(durationtools.Duration(-1, 2), 1)
    b = timeintervaltools.TimeInterval(2, durationtools.Duration(7, 3))
    tree = timeintervaltools.TimeIntervalTree([a, b])
    rational = 3
    result = tree.scale_to_rational(rational)
    assert result.duration == 3
    assert [x.signature for x in result] == \
        [(Offset(-1, 2), Offset(37, 34)), 
        (Offset(73, 34), Offset(5, 2))]


def test_TimeIntervalTree_scale_to_rational_03():
    a = timeintervaltools.TimeInterval(durationtools.Duration(-1, 2), 1)
    b = timeintervaltools.TimeInterval(2, durationtools.Duration(7, 3))
    tree = timeintervaltools.TimeIntervalTree([a, b])
    rational = -1
    py.test.raises(AssertionError,
        "result = tree.scale_to_rational(rational)")


def test_TimeIntervalTree_scale_to_rational_04():
    a = timeintervaltools.TimeInterval(durationtools.Duration(-1, 2), 1)
    b = timeintervaltools.TimeInterval(2, durationtools.Duration(7, 3))
    tree = timeintervaltools.TimeIntervalTree([a, b])
    rational = 0
    py.test.raises(AssertionError,
        "result = tree.scale_to_rational(rational)")
