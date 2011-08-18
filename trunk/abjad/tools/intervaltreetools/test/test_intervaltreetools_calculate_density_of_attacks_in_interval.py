from abjad import Fraction
from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_calculate_density_of_attacks_in_interval_01():
    tree = IntervalTree(_make_test_intervals())
    assert calculate_density_of_releases_in_interval(tree,
        BoundedInterval(-2, -1)) == 0


def test_intervaltreetools_calculate_density_of_attacks_in_interval_02():
    tree = IntervalTree(_make_test_intervals())
    assert calculate_density_of_releases_in_interval(tree,
        BoundedInterval(0, 37)) == Fraction(12, 37)
