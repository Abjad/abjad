from fractions import Fraction
from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import TimeInterval
from abjad.tools.timeintervaltools import TimeIntervalTree


def test_TimeIntervalTree_scale_by_rational_01():
    t1 = TimeInterval(0, 4)
    t2 = TimeInterval(2, 6)
    t3 = TimeInterval(1, 8)

    tree = TimeIntervalTree([t1, t2, t3])
    scalar = Fraction(1, 2)
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
    t0 = TimeInterval(-3, -1)
    t1 = TimeInterval(0, 4)
    t2 = TimeInterval(2, 6)
    t3 = TimeInterval(1, 8)

    tree = TimeIntervalTree([t0, t1, t2, t3])
    scalar = Fraction(1, 2)
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

    
