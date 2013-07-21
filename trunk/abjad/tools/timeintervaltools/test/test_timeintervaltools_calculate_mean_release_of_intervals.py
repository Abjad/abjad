from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_calculate_mean_release_of_intervals_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    release = calculate_mean_release_of_intervals(tree)
    assert release == Offset(sum([x.stop_offset for x in tree]), len(tree))


def test_timeintervaltools_calculate_mean_release_of_intervals_02():
    tree = TimeIntervalTree([])
    release = calculate_mean_release_of_intervals(tree)
    assert release is None
