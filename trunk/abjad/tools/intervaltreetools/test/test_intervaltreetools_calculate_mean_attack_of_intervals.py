from abjad.tools.durationtools import Offset
from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_calculate_mean_attack_of_intervals_01():
    tree = IntervalTree(_make_test_intervals())
    attack = calculate_mean_attack_of_intervals(tree)
    assert attack == Offset(sum([x.start for x in tree]), len(tree))


def test_intervaltreetools_calculate_mean_attack_of_intervals_02():
    tree = IntervalTree([])
    attack = calculate_mean_attack_of_intervals(tree)
    assert attack is None
