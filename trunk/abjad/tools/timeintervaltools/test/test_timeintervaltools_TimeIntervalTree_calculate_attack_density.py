# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeIntervalTree_calculate_attack_density_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    attack_density = tree.calculate_attack_density(
        bounding_interval=timeintervaltools.TimeInterval(-2, -1))
    assert attack_density == 0


def test_timeintervaltools_TimeIntervalTree_calculate_attack_density_02():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    attack_density = tree.calculate_attack_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 37))
    assert attack_density == Multiplier(12, 37)
