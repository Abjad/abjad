from abjad import *
import py.test


def test_TimeIntervalTree_scale_interval_durations_to_rational_01():
    a = timeintervaltools.TimeInterval(0, 10, {'a': 1})
    b = timeintervaltools.TimeInterval(Fraction(5, 3), 10, {'b': 2})
    c = timeintervaltools.TimeInterval(5, Fraction(61, 7), {'c': 3})
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_to_rational(scalar)
    assert scaled == timeintervaltools.TimeIntervalTree([
        timeintervaltools.TimeInterval(Offset(0, 1), Offset(5, 2), {'a': 1}),
        timeintervaltools.TimeInterval(Offset(5, 3), Offset(25, 6), {'b': 2}),
        timeintervaltools.TimeInterval(Offset(5, 1), Offset(15, 2), {'c': 3})
        ])

def test_TimeIntervalTree_scale_interval_durations_to_rational_02():
    tree = timeintervaltools.TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_by_rational(scalar)
    assert scaled == tree
