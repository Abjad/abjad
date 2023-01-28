import pytest

import abjad


def test_Duration__group_by_implied_prolation_01():
    with pytest.raises(Exception):
        abjad.makers._group_by_implied_prolation([])


def test_Duration__group_by_implied_prolation_02():
    fractions = [(1, 4)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [[(1, 4)]]


def test_Duration__group_by_implied_prolation_03():
    fractions = [(1, 4), (1, 4), (1, 8)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [
            (1, 4),
            (1, 4),
            (1, 8),
        ]
    ]


def test_Duration__group_by_implied_prolation_04():
    fractions = [(1, 4), (1, 3), (1, 8)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [(1, 4)],
        [(1, 3)],
        [(1, 8)],
    ]


def test_Duration__group_by_implied_prolation_05():
    fractions = [(1, 4), (1, 2), (1, 3)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [(1, 4), (1, 2)],
        [(1, 3)],
    ]


def test_Duration__group_by_implied_prolation_06():
    fractions = [(1, 4), (1, 2), (1, 3), (1, 6), (1, 5)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [(1, 4), (1, 2)],
        [(1, 3), (1, 6)],
        [(1, 5)],
    ]


def test_Duration__group_by_implied_prolation_07():
    fractions = [(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [
            (1, 24),
            (2, 24),
            (3, 24),
            (4, 24),
            (5, 24),
            (6, 24),
        ]
    ]
