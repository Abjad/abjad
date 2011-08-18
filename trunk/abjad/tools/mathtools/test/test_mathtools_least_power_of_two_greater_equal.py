from abjad import *
from abjad.tools import mathtools
import py.test


def test_mathtools_least_power_of_two_greater_equal_01():
    '''Return least integer power of two
        greater than or equal to n.'''

    assert mathtools.least_power_of_two_greater_equal(1) == 1
    assert mathtools.least_power_of_two_greater_equal(2) == 2
    assert mathtools.least_power_of_two_greater_equal(3) == 4
    assert mathtools.least_power_of_two_greater_equal(4) == 4
    assert mathtools.least_power_of_two_greater_equal(5) == 8
    assert mathtools.least_power_of_two_greater_equal(6) == 8
    assert mathtools.least_power_of_two_greater_equal(7) == 8
    assert mathtools.least_power_of_two_greater_equal(8) == 8
    assert mathtools.least_power_of_two_greater_equal(9) == 16
    assert mathtools.least_power_of_two_greater_equal(10) == 16
    assert mathtools.least_power_of_two_greater_equal(11) == 16
    assert mathtools.least_power_of_two_greater_equal(12) == 16



def test_mathtools_least_power_of_two_greater_equal_02():
    '''Raise TypeError on nonnumeric n.
        Raise ValueError on nonpositive n.'''

    assert py.test.raises(
        TypeError, "mathtools.least_power_of_two_greater_equal('foo')")
    assert py.test.raises(
        ValueError, 'mathtools.least_power_of_two_greater_equal(0)')
    assert py.test.raises(
        ValueError, 'mathtools.least_power_of_two_greater_equal(-1)')


def test_mathtools_least_power_of_two_greater_equal_03():
    '''Optional offset keyword allows for the next to greatest
        integer power of two, etc.'''

    assert mathtools.least_power_of_two_greater_equal(1, 1) == 2
    assert mathtools.least_power_of_two_greater_equal(2, 1) == 4
    assert mathtools.least_power_of_two_greater_equal(3, 1) == 8
    assert mathtools.least_power_of_two_greater_equal(4, 1) == 8
    assert mathtools.least_power_of_two_greater_equal(5, 1) == 16
    assert mathtools.least_power_of_two_greater_equal(6, 1) == 16
    assert mathtools.least_power_of_two_greater_equal(7, 1) == 16
    assert mathtools.least_power_of_two_greater_equal(8, 1) == 16
    assert mathtools.least_power_of_two_greater_equal(9, 1) == 32
    assert mathtools.least_power_of_two_greater_equal(10, 1) == 32
    assert mathtools.least_power_of_two_greater_equal(11, 1) == 32
    assert mathtools.least_power_of_two_greater_equal(12, 1) == 32
