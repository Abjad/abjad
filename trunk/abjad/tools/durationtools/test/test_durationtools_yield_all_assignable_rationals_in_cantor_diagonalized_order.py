from abjad import *
from abjad.tools import durationtools


def test_durationtools_yield_all_assignable_rationals_in_cantor_diagonalized_order_01():

    generator = durationtools.yield_all_assignable_rationals_in_cantor_diagonalized_order()

    assert generator.next() == Fraction(1, 1)
    assert generator.next() == Fraction(2, 1)
    assert generator.next() == Fraction(1, 2)
    assert generator.next() == Fraction(3, 1)
    assert generator.next() == Fraction(4, 1)
    assert generator.next() == Fraction(3, 2)
    assert generator.next() == Fraction(1, 4)
    assert generator.next() == Fraction(6, 1)
    assert generator.next() == Fraction(3, 4)
    assert generator.next() == Fraction(7, 1)
    assert generator.next() == Fraction(8, 1)
    assert generator.next() == Fraction(7, 2)
    assert generator.next() == Fraction(1, 8)
    assert generator.next() == Fraction(7, 4)
    assert generator.next() == Fraction(3, 8)
    assert generator.next() == Fraction(12, 1)
