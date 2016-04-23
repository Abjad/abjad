# -*- coding: utf-8
from abjad import *


def test_rhythmmakertools_TieSpecifier_split_at_indices_01():
    # tie all
    group = [1, 1, 1]
    pattern = patterntools.select_all()
    tie_specifier = rhythmmakertools.TieSpecifier(
        tie_consecutive_notes=pattern
        )
    subgroups = tie_specifier._split_at_indices(group)
    assert subgroups == [[1, 1, 1]]


def test_rhythmmakertools_TieSpecifier_split_at_indices_02():
    # tie none
    group = [1, 1, 1]
    pattern = patterntools.select_all(inverted=True)
    tie_specifier = rhythmmakertools.TieSpecifier(
        tie_consecutive_notes=pattern
        )
    subgroups = tie_specifier._split_at_indices(group)
    assert subgroups == [[1], [1], [1]]


def test_rhythmmakertools_TieSpecifier_split_at_indices_03():
    # too short for pattern to be effective
    group = [1, 1]
    pattern = patterntools.Pattern(indices=[2], period=3)
    tie_specifier = rhythmmakertools.TieSpecifier(
        tie_consecutive_notes=pattern
        )
    subgroups = tie_specifier._split_at_indices(group)
    assert subgroups == [[1], [1]]


def test_rhythmmakertools_TieSpecifier_split_at_indices_04():
    # tie every other, even
    group = [1] * 6
    pattern = patterntools.select_every(indices=[1], period=2)
    tie_specifier = rhythmmakertools.TieSpecifier(
        tie_consecutive_notes=pattern
        )
    subgroups = tie_specifier._split_at_indices(group)
    assert subgroups == [[1, 1], [1, 1], [1, 1]]


def test_rhythmmakertools_TieSpecifier_split_at_indices_05():
    # tie every other, odd
    group = [1] * 7
    pattern = patterntools.select_every(indices=[1], period=2)
    tie_specifier = rhythmmakertools.TieSpecifier(
        tie_consecutive_notes=pattern
        )
    subgroups = tie_specifier._split_at_indices(group)
    assert subgroups == [[1, 1], [1, 1], [1, 1], [1]]

def test_rhythmmakertools_TieSpecifier_split_at_indices_06():
    # groups of 3 and 2, cyclic, incomplete
    group = [1] * 9
    pattern = patterntools.select_every(indices=[1, 2, 4], period=5)
    tie_specifier = rhythmmakertools.TieSpecifier(
        tie_consecutive_notes=pattern
    )
    subgroups = tie_specifier._split_at_indices(group)
    assert subgroups == [[1, 1, 1], [1, 1], [1, 1, 1], [1]]
