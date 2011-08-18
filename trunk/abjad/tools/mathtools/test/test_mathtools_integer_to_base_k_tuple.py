from abjad import *
from abjad.tools import mathtools


def test_mathtools_integer_to_base_k_tuple_01():

    assert mathtools.integer_to_base_k_tuple(0, 2) == (0, )
    assert mathtools.integer_to_base_k_tuple(1, 2) == (1, )
    assert mathtools.integer_to_base_k_tuple(2, 2) == (1, 0)
    assert mathtools.integer_to_base_k_tuple(3, 2) == (1, 1)
    assert mathtools.integer_to_base_k_tuple(4, 2) == (1, 0, 0)
    assert mathtools.integer_to_base_k_tuple(5, 2) == (1, 0, 1)
    assert mathtools.integer_to_base_k_tuple(6, 2) == (1, 1, 0)
    assert mathtools.integer_to_base_k_tuple(7, 2) == (1, 1, 1)
    assert mathtools.integer_to_base_k_tuple(8, 2) == (1, 0, 0, 0)


def test_mathtools_integer_to_base_k_tuple_02():

    assert mathtools.integer_to_base_k_tuple(1066, 10) == (1, 0, 6, 6)
    assert mathtools.integer_to_base_k_tuple(1987, 10) == (1, 9, 8, 7)
    assert mathtools.integer_to_base_k_tuple(3012, 10) == (3, 0, 1, 2)
