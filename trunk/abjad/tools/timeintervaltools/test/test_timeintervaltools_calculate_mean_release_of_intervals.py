from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_timeintervaltools_calculate_mean_release_of_intervals_01():
    tree = TimeIntervalTree(_make_test_intervals())
    release = calculate_mean_release_of_intervals(tree)
    assert release == Offset(sum([x.stop for x in tree]), len(tree))


def test_timeintervaltools_calculate_mean_release_of_intervals_02():
    tree = TimeIntervalTree([])
    release = calculate_mean_release_of_intervals(tree)
    assert release is None
