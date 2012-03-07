from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_timeintervaltools_calculate_mean_attack_of_intervals_01():
    tree = TimeIntervalTree(_make_test_intervals())
    attack = calculate_mean_attack_of_intervals(tree)
    assert attack == Offset(sum([x.start for x in tree]), len(tree))


def test_timeintervaltools_calculate_mean_attack_of_intervals_02():
    tree = TimeIntervalTree([])
    attack = calculate_mean_attack_of_intervals(tree)
    assert attack is None
