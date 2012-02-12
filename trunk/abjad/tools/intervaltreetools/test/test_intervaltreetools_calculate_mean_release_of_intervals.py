from abjad.tools.durationtools import Offset
from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_calculate_mean_release_of_intervals_01():
    tree = IntervalTree(_make_test_intervals())
    release = calculate_mean_release_of_intervals(tree)
    assert release == Offset(sum([x.stop for x in tree]), len(tree))


def test_intervaltreetools_calculate_mean_release_of_intervals_02():
    tree = IntervalTree([])
    release = calculate_mean_release_of_intervals(tree)
    assert release is None
