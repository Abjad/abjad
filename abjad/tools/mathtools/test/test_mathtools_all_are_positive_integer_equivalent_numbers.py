# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_positive_integer_equivalent_numbers_01():

    assert mathtools.all_are_positive_integer_equivalent_numbers(
        [Fraction(4, 2), 2.0, 2])


def test_mathtools_all_are_positive_integer_equivalent_numbers_02():

    assert not mathtools.all_are_positive_integer_equivalent_numbers(
        [Fraction(5, 2), 2.5, -2, 0])
