from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction


def test_intervaltreetools_calculate_sustain_centroid_of_intervals_01():
    tree = IntervalTree(_make_test_intervals())
    result = calculate_sustain_centroid_of_intervals(tree)
    assert result == Fraction(1619, 90)


def test_intervaltreetools_calculate_sustain_centroid_of_intervals_02():
    tree = IntervalTree([])
    result = calculate_sustain_centroid_of_intervals(tree)
    assert result is None
