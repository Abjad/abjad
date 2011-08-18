from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_nonnegative_integer_power_of_two_01():
    '''Return True when expr is an integer or Duration power of two,
        otherwise False.'''

    assert mathtools.is_nonnegative_integer_power_of_two(0)
    assert mathtools.is_nonnegative_integer_power_of_two(1)
    assert mathtools.is_nonnegative_integer_power_of_two(2)
    assert not mathtools.is_nonnegative_integer_power_of_two(3)
    assert mathtools.is_nonnegative_integer_power_of_two(4)
    assert not mathtools.is_nonnegative_integer_power_of_two(5)
    assert not mathtools.is_nonnegative_integer_power_of_two(6)
    assert not mathtools.is_nonnegative_integer_power_of_two(7)
    assert mathtools.is_nonnegative_integer_power_of_two(8)
    assert not mathtools.is_nonnegative_integer_power_of_two(9)
    assert not mathtools.is_nonnegative_integer_power_of_two(10)
    assert not mathtools.is_nonnegative_integer_power_of_two(11)
    assert not mathtools.is_nonnegative_integer_power_of_two(12)


def test_mathtools_is_nonnegative_integer_power_of_two_02():
    '''Return True when expr is an integer or Duration power of two,
        otherwise False.'''

    assert mathtools.is_nonnegative_integer_power_of_two(0)
    assert not mathtools.is_nonnegative_integer_power_of_two(-1)
    assert not mathtools.is_nonnegative_integer_power_of_two(-2)
    assert not mathtools.is_nonnegative_integer_power_of_two(-3)
    assert not mathtools.is_nonnegative_integer_power_of_two(-4)
    assert not mathtools.is_nonnegative_integer_power_of_two(-5)
    assert not mathtools.is_nonnegative_integer_power_of_two(-6)
    assert not mathtools.is_nonnegative_integer_power_of_two(-7)
    assert not mathtools.is_nonnegative_integer_power_of_two(-8)
    assert not mathtools.is_nonnegative_integer_power_of_two(-9)
    assert not mathtools.is_nonnegative_integer_power_of_two(-10)
    assert not mathtools.is_nonnegative_integer_power_of_two(-11)
    assert not mathtools.is_nonnegative_integer_power_of_two(-12)


def test_mathtools_is_nonnegative_integer_power_of_two_03():
    '''Return True when expr is an integer or Duration power of two,
        otherwise False.'''

    assert mathtools.is_nonnegative_integer_power_of_two(Duration(0))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(1))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(2))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(3))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(4))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(5))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(6))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(7))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(8))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(9))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(10))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(11))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(12))


def test_mathtools_is_nonnegative_integer_power_of_two_04():
    '''Return True when expr is an integer or Duration power of two,
        otherwise False.'''

    assert mathtools.is_nonnegative_integer_power_of_two(Duration(1, 1))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(1, 2))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 3))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(1, 4))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 5))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 6))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 7))
    assert mathtools.is_nonnegative_integer_power_of_two(Duration(1, 8))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 9))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 10))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 11))
    assert not mathtools.is_nonnegative_integer_power_of_two(Duration(1, 12))
