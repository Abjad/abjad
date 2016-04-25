# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_greatest_power_of_two_less_equal_01():
    r'''Returns greatest integer power of two
    less than or equal to n.
    '''

    assert mathtools.greatest_power_of_two_less_equal(1) == 1
    assert mathtools.greatest_power_of_two_less_equal(2) == 2
    assert mathtools.greatest_power_of_two_less_equal(3) == 2
    assert mathtools.greatest_power_of_two_less_equal(4) == 4
    assert mathtools.greatest_power_of_two_less_equal(5) == 4
    assert mathtools.greatest_power_of_two_less_equal(6) == 4
    assert mathtools.greatest_power_of_two_less_equal(7) == 4
    assert mathtools.greatest_power_of_two_less_equal(8) == 8
    assert mathtools.greatest_power_of_two_less_equal(9) == 8
    assert mathtools.greatest_power_of_two_less_equal(10) == 8
    assert mathtools.greatest_power_of_two_less_equal(11) == 8
    assert mathtools.greatest_power_of_two_less_equal(12) == 8


def test_mathtools_greatest_power_of_two_less_equal_02():
    r'''Raise TypeError on nonnumeric n.
    Raise ValueError on nonpositive n.
    '''

    statement = "mathtools.greatest_power_of_two_less_equal('foo')"
    assert pytest.raises(TypeError, statement)
    statement = 'mathtools.greatest_power_of_two_less_equal(0)'
    assert pytest.raises(ValueError, statement)
    statement = 'mathtools.greatest_power_of_two_less_equal(-1)'
    assert pytest.raises(ValueError, statement)


def test_mathtools_greatest_power_of_two_less_equal_03():
    r'''Optional offset keyword allows for the next to greatest
    integer power of two, etc.
    '''

    assert mathtools.greatest_power_of_two_less_equal(1, 1) == 0.5
    assert mathtools.greatest_power_of_two_less_equal(2, 1) == 1
    assert mathtools.greatest_power_of_two_less_equal(3, 1) == 1
    assert mathtools.greatest_power_of_two_less_equal(4, 1) == 2
    assert mathtools.greatest_power_of_two_less_equal(5, 1) == 2
    assert mathtools.greatest_power_of_two_less_equal(6, 1) == 2
    assert mathtools.greatest_power_of_two_less_equal(7, 1) == 2
    assert mathtools.greatest_power_of_two_less_equal(8, 1) == 4
    assert mathtools.greatest_power_of_two_less_equal(9, 1) == 4
    assert mathtools.greatest_power_of_two_less_equal(10, 1) == 4
    assert mathtools.greatest_power_of_two_less_equal(11, 1) == 4
    assert mathtools.greatest_power_of_two_less_equal(12, 1) == 4
