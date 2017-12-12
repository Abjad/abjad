import pytest
import abjad


def test_datastructuretools_Duration__group_by_implied_prolation_01():

    string = 'Duation._group_by_implied_prolation([])'
    assert pytest.raises(Exception, string)


def test_datastructuretools_Duration__group_by_implied_prolation_02():

    fractions = [(1, 4)]
    duration = abjad.Duration._group_by_implied_prolation(fractions)
    assert duration == [[abjad.NonreducedFraction(1, 4)]]


def test_datastructuretools_Duration__group_by_implied_prolation_03():

    fractions = [(1, 4), (1, 4), (1, 8)]
    duration = abjad.Duration._group_by_implied_prolation(fractions)
    assert duration == [[
        abjad.NonreducedFraction(1, 4),
        abjad.NonreducedFraction(1, 4),
        abjad.NonreducedFraction(1, 8),
        ]]


def test_datastructuretools_Duration__group_by_implied_prolation_04():

    fractions = [(1, 4), (1, 3), (1, 8)]
    duration = abjad.Duration._group_by_implied_prolation(fractions)
    assert duration == [
        [abjad.NonreducedFraction(1, 4)],
        [abjad.NonreducedFraction(1, 3)],
        [abjad.NonreducedFraction(1, 8)],
        ]


def test_datastructuretools_Duration__group_by_implied_prolation_05():

    fractions = [(1, 4), (1, 2), (1, 3)]
    duration = abjad.Duration._group_by_implied_prolation(fractions)
    assert duration == [
        [abjad.NonreducedFraction(1, 4),
            abjad.NonreducedFraction(1, 2)],
        [abjad.NonreducedFraction(1, 3)],
        ]


def test_datastructuretools_Duration__group_by_implied_prolation_06():

    fractions = [(1, 4), (1, 2), (1, 3), (1, 6), (1, 5)]
    duration = abjad.Duration._group_by_implied_prolation(fractions)
    assert duration == [
        [abjad.NonreducedFraction(1, 4),
            abjad.NonreducedFraction(1, 2)],
        [abjad.NonreducedFraction(1, 3),
            abjad.NonreducedFraction(1, 6)],
        [abjad.NonreducedFraction(1, 5)],
        ]


def test_datastructuretools_Duration__group_by_implied_prolation_07():

    fractions = [(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]
    duration = abjad.Duration._group_by_implied_prolation(fractions)
    assert duration == [[
        abjad.NonreducedFraction(1, 24),
        abjad.NonreducedFraction(2, 24),
        abjad.NonreducedFraction(3, 24),
        abjad.NonreducedFraction(4, 24),
        abjad.NonreducedFraction(5, 24),
        abjad.NonreducedFraction(6, 24),
        ]]
