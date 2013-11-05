# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeIntervalTree_calculate_mean_attack_offset_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    mean_attack_offset = tree.calculate_mean_attack_offset()
    assert mean_attack_offset == Offset(sum(x.start_offset for x in tree), len(tree))


def test_timeintervaltools_TimeIntervalTree_calculate_mean_attack_offset_02():
    tree = timeintervaltools.TimeIntervalTree([])
    mean_attack_offset = tree.calculate_mean_attack_offset()
    assert mean_attack_offset is None
