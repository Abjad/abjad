# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_integer_equivalent_numbers_01():

    numbers = [1, 2, 3.0, Fraction(4)]
    assert mathtools.all_are_integer_equivalent_numbers(numbers)


def test_mathtools_all_are_integer_equivalent_numbers_02():

    numbers = [1, 2, 3.5, 4]
    assert not mathtools.all_are_integer_equivalent_numbers(numbers)

    numbers = [1, 2, 3, Fraction(4, 11)]
    assert not mathtools.all_are_integer_equivalent_numbers(numbers)

    assert not mathtools.all_are_integer_equivalent_numbers(7)

    assert not mathtools.all_are_integer_equivalent_numbers('foo')
