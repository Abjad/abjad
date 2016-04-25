# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_nonnegative_integer_equivalent_numbers_01():

    numbers = [0, 0.0, Fraction(0)]
    assert mathtools.all_are_nonnegative_integer_equivalent_numbers(
        numbers)

    numbers = [2, 3, Fraction(4)]
    assert mathtools.all_are_nonnegative_integer_equivalent_numbers(
        numbers)


def test_mathtools_all_are_nonnegative_integer_equivalent_numbers_02():

    numbers = [-1, -2.0, Fraction(-3)]
    assert not mathtools.all_are_nonnegative_integer_equivalent_numbers(
        numbers)
