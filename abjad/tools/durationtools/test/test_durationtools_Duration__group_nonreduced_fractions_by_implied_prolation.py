# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.durationtools import Duration
from abjad.tools.mathtools import NonreducedFraction


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_01():
    string = 'Duation._group_nonreduced_fractions_by_implied_prolation([])'
    assert pytest.raises(Exception, string)


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_02():
    fractions = [(1, 4)]
    duration = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert duration == [[NonreducedFraction(1, 4)]]


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_03():
    fractions = [(1, 4), (1, 4), (1, 8)]
    duration = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert duration == [[
        NonreducedFraction(1, 4), 
        NonreducedFraction(1, 4), 
        NonreducedFraction(1, 8),
        ]]


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_04():
    fractions = [(1, 4), (1, 3), (1, 8)]
    duration = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert duration == [
        [NonreducedFraction(1, 4)], 
        [NonreducedFraction(1, 3)], 
        [NonreducedFraction(1, 8)],
        ]


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_05():
    fractions = [(1, 4), (1, 2), (1, 3)]
    duration = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert duration == [
        [NonreducedFraction(1, 4), NonreducedFraction(1, 2)], 
        [NonreducedFraction(1, 3)],
        ]


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_06():
    fractions = [(1, 4), (1, 2), (1, 3), (1, 6), (1, 5)]
    duration = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert duration == [
        [NonreducedFraction(1, 4), NonreducedFraction(1, 2)], 
        [NonreducedFraction(1, 3), NonreducedFraction(1, 6)], 
        [NonreducedFraction(1, 5)],
        ]


def test_durationtools_Duration__group_nonreduced_fractions_by_implied_prolation_07():
    fractions = [(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]
    duration = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert duration == [[
        NonreducedFraction(1, 24), 
        NonreducedFraction(2, 24), 
        NonreducedFraction(3, 24), 
        NonreducedFraction(4, 24), 
        NonreducedFraction(5, 24), 
        NonreducedFraction(6, 24),
        ]]
