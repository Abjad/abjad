import py
from abjad.tools.intervaltreetools import IntervalTree
from abjad.tools.intervaltreetools import calculate_min_mean_and_max_durations_of_intervals
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction


def test_intervaltreetools_calculate_min_mean_and_max_durations_of_intervals_01():
    tree = IntervalTree([])
    result = calculate_min_mean_and_max_durations_of_intervals(tree)
    assert result is None


def test_intervaltreetools_calculate_min_mean_and_max_durations_of_intervals_02():
    tree = IntervalTree(_make_test_intervals())
    result = calculate_min_mean_and_max_durations_of_intervals(tree)
    assert result == (1, Fraction(15, 4), 8)
