from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_calculate_sustain_centroid_of_intervals_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    result = calculate_sustain_centroid_of_intervals(tree)
    assert result == Fraction(1619, 90)


def test_timeintervaltools_calculate_sustain_centroid_of_intervals_02():
    tree = TimeIntervalTree([])
    result = calculate_sustain_centroid_of_intervals(tree)
    assert result is None
