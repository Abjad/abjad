from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_calculate_mean_attack_of_intervals_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    attack = calculate_mean_attack_of_intervals(tree)
    assert attack == Offset(sum([x.start for x in tree]), len(tree))


def test_timeintervaltools_calculate_mean_attack_of_intervals_02():
    tree = TimeIntervalTree([])
    attack = calculate_mean_attack_of_intervals(tree)
    assert attack is None
