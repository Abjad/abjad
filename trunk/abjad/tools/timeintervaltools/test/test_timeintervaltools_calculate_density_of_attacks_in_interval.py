from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_calculate_density_of_attacks_in_interval_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    assert calculate_density_of_releases_in_interval(tree,
        TimeInterval(-2, -1)) == 0


def test_timeintervaltools_calculate_density_of_attacks_in_interval_02():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    assert calculate_density_of_releases_in_interval(tree,
        TimeInterval(0, 37)) == Fraction(12, 37)
