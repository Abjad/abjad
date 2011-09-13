from abjad import *
from abjad.tools import durationtools


def test_durationtools_yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order_01():

    pairs = durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Fraction(1, 8))

    assert pairs == (
        (Fraction(1, 1), Fraction(1, 8)),
        (Fraction(2, 3), Fraction(3, 16)),
        (Fraction(4, 3), Fraction(3, 32)),
        (Fraction(4, 7), Fraction(7, 32)),
        (Fraction(8, 7), Fraction(7, 64)),
        (Fraction(8, 15), Fraction(15, 64)),
        (Fraction(16, 15), Fraction(15, 128)),
        (Fraction(16, 31), Fraction(31, 128)))


def test_durationtools_yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order_02():


    pairs = durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Fraction(1, 12))

    assert pairs == (
        (Fraction(2, 3), Fraction(1, 8)),
        (Fraction(4, 3), Fraction(1, 16)),
        (Fraction(8, 9), Fraction(3, 32)),
        (Fraction(16, 9), Fraction(3, 64)),
        (Fraction(16, 21), Fraction(7, 64)),
        (Fraction(32, 21), Fraction(7, 128)),
        (Fraction(32, 45), Fraction(15, 128)))


def test_durationtools_yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order_03():


    pairs = durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Fraction(5, 48))

    assert pairs == (
        (Fraction(5, 6), Fraction(1, 8)),
        (Fraction(5, 3), Fraction(1, 16)),
        (Fraction(5, 9), Fraction(3, 16)),
        (Fraction(10, 9), Fraction(3, 32)),
        (Fraction(20, 21), Fraction(7, 64)),
        (Fraction(40, 21), Fraction(7, 128)),
        (Fraction(8, 9), Fraction(15, 128)))
