from abjad import *
from abjad.tools import durationtools


def test_durationtools_yield_all_positive_integer_pairs_in_cantor_diagonalized_order_01():

    generator = durationtools.yield_all_positive_integer_pairs_in_cantor_diagonalized_order()

    assert generator.next() == (1, 1)
    assert generator.next() == (2, 1)
    assert generator.next() == (1, 2)
    assert generator.next() == (1, 3)
    assert generator.next() == (2, 2)
    assert generator.next() == (3, 1)
    assert generator.next() == (4, 1)
    assert generator.next() == (3, 2)
    assert generator.next() == (2, 3)
    assert generator.next() == (1, 4)
    assert generator.next() == (1, 5)
    assert generator.next() == (2, 4)
