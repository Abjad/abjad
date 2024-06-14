import pytest

import abjad


def test_makers__group_by_implied_prolation_01():
    with pytest.raises(Exception):
        abjad.makers._group_by_implied_prolation([])


def test_makers__group_by_implied_prolation_02():
    fractions = [(1, 4)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [[(1, 4)]]


def test_makers__group_by_implied_prolation_03():
    fractions = [(1, 4), (1, 4), (1, 8)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [
            (1, 4),
            (1, 4),
            (1, 8),
        ]
    ]


def test_makers__group_by_implied_prolation_04():
    fractions = [(1, 4), (1, 3), (1, 8)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [(1, 4)],
        [(1, 3)],
        [(1, 8)],
    ]


def test_makers__group_by_implied_prolation_05():
    fractions = [(1, 4), (1, 2), (1, 3)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [(1, 4), (1, 2)],
        [(1, 3)],
    ]


def test_makers__group_by_implied_prolation_06():
    fractions = [(1, 4), (1, 2), (1, 3), (1, 6), (1, 5)]
    duration = abjad.makers._group_by_implied_prolation(fractions)
    assert duration == [
        [(1, 4), (1, 2)],
        [(1, 3), (1, 6)],
        [(1, 5)],
    ]


def test_makers__group_by_implied_prolation_07():
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


def test_makers_tuplet_from_ratio_and_pair_01():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 4), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 7/6
        {
            c'16
            c'8
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_02():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, 2, 4), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 4/3
        {
            c'16
            c'16
            c'8
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_03():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((-2, 3, 7), (7, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 12/7
        {
            r8
            c'8.
            c'4..
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_04():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((7, 7, -4, -1), (1, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tuplet 19/16
        {
            c'16..
            c'16..
            r16
            r64
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_05():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_06():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_07():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((4, 8, 8), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_08():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((8, 16, 16), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/3
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_09():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (3, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/3
        {
            c'16
            c'8
            c'8
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_10():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/3
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_11():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (12, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_12():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((2, 4, 4), (24, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_13():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 2))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'2
            c'1
            c'1
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_14():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 4))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'4
            c'2
            c'2
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_15():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 8))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'8
            c'4
            c'4
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_16():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 2, 2), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/6
        {
            c'16
            c'8
            c'8
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_17():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, -1, -1), (3, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 1/1
        {
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_18():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, -1, -1), (4, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 1/1
        {
            c'16
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_19():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, 1, -1, -1), (5, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 1/1
        {
            c'16
            c'16
            c'16
            r16
            r16
        }
        """
    )


def test_makers_tuplet_from_ratio_and_pair_20():
    tuplet = abjad.makers.tuplet_from_ratio_and_pair((1, 1, 1, 1, -1, -1), (6, 16))

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 1/1
        {
            c'16
            c'16
            c'16
            c'16
            r16
            r16
        }
        """
    )
