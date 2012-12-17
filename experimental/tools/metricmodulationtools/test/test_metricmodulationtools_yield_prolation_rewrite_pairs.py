from abjad import *
from experimental.tools import *


def test_metricmodulationtools_yield_prolation_rewrite_pairs_01():

    pairs = metricmodulationtools.yield_prolation_rewrite_pairs(Duration(1, 8))

    assert pairs == (
        (Multiplier(1, 1), Duration(1, 8)),
        (Multiplier(2, 3), Duration(3, 16)),
        (Multiplier(4, 3), Duration(3, 32)),
        (Multiplier(4, 7), Duration(7, 32)),
        (Multiplier(8, 7), Duration(7, 64)),
        (Multiplier(8, 15), Duration(15, 64)),
        (Multiplier(16, 15), Duration(15, 128)),
        (Multiplier(16, 31), Duration(31, 128)))


def test_metricmodulationtools_yield_prolation_rewrite_pairs_02():


    pairs = metricmodulationtools.yield_prolation_rewrite_pairs(Duration(1, 12))

    assert pairs == (
        (Multiplier(2, 3), Duration(1, 8)),
        (Multiplier(4, 3), Duration(1, 16)),
        (Multiplier(8, 9), Duration(3, 32)),
        (Multiplier(16, 9), Duration(3, 64)),
        (Multiplier(16, 21), Duration(7, 64)),
        (Multiplier(32, 21), Duration(7, 128)),
        (Multiplier(32, 45), Duration(15, 128)))


def test_metricmodulationtools_yield_prolation_rewrite_pairs_03():


    pairs = metricmodulationtools.yield_prolation_rewrite_pairs(Duration(5, 48))

    assert pairs == (
        (Multiplier(5, 6), Duration(1, 8)),
        (Multiplier(5, 3), Duration(1, 16)),
        (Multiplier(5, 9), Duration(3, 16)),
        (Multiplier(10, 9), Duration(3, 32)),
        (Multiplier(20, 21), Duration(7, 64)),
        (Multiplier(40, 21), Duration(7, 128)),
        (Multiplier(8, 9), Duration(15, 128)))
