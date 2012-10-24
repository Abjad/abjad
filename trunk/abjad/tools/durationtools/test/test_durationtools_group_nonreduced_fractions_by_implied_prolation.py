import py
from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_01():
    assert py.test.raises(
        AssertionError, 'durationtools.group_nonreduced_fractions_by_implied_prolation([])')


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_02():
    t = durationtools.group_nonreduced_fractions_by_implied_prolation([(1, 4)])
    assert t == [[NonreducedFraction(1, 4)]]


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_03():
    t = durationtools.group_nonreduced_fractions_by_implied_prolation([(1, 4), (1, 4), (1, 8)])
    assert t == [[NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]]


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_04():
    t = durationtools.group_nonreduced_fractions_by_implied_prolation([(1, 4), (1, 3), (1, 8)])
    assert t == [[NonreducedFraction(1, 4)], [NonreducedFraction(1, 3)], [NonreducedFraction(1, 8)]]


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_05():
    t = durationtools.group_nonreduced_fractions_by_implied_prolation([(1, 4), (1, 2), (1, 3)])
    assert t == [[NonreducedFraction(1, 4), NonreducedFraction(1, 2)], [NonreducedFraction(1, 3)]]


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_06():
    t = durationtools.group_nonreduced_fractions_by_implied_prolation([(1, 4), (1, 2), (1, 3), (1, 6),
        (1, 5)])
    assert t == [[NonreducedFraction(1, 4), NonreducedFraction(1, 2)], [NonreducedFraction(1, 3), NonreducedFraction(1, 6)], [NonreducedFraction(1, 5)]]


def test_durationtools_group_nonreduced_fractions_by_implied_prolation_07():
    t = durationtools.group_nonreduced_fractions_by_implied_prolation([(1, 24), (2, 24), (3, 24),
        (4, 24), (5, 24), (6, 24)])
    assert t == [[NonreducedFraction(1, 24), NonreducedFraction(2, 24), NonreducedFraction(3, 24), NonreducedFraction(4, 24), NonreducedFraction(5, 24), NonreducedFraction(6, 24)]]
