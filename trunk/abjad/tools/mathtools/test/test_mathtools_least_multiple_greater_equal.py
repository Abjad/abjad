from abjad import *
from abjad.tools import mathtools


def test_mathtools_least_multiple_greater_equal_01():
    '''Return the least multiple of m greater than or equal to n.'''

    assert mathtools.least_multiple_greater_equal(10, 0) == 0
    assert mathtools.least_multiple_greater_equal(10, 1) == 10
    assert mathtools.least_multiple_greater_equal(10, 2) == 10
    assert mathtools.least_multiple_greater_equal(10, 13) == 20
    assert mathtools.least_multiple_greater_equal(10, 28) == 30
    assert mathtools.least_multiple_greater_equal(10, 40) == 40
    assert mathtools.least_multiple_greater_equal(10, 41) == 50


def test_mathtools_least_multiple_greater_equal_02():
    '''Return the least multiple of m greater than or equal to n.'''

    assert mathtools.least_multiple_greater_equal(7, 0) == 0
    assert mathtools.least_multiple_greater_equal(7, 1) == 7
    assert mathtools.least_multiple_greater_equal(7, 2) == 7
    assert mathtools.least_multiple_greater_equal(7, 13) == 14
    assert mathtools.least_multiple_greater_equal(7, 28) == 28
    assert mathtools.least_multiple_greater_equal(7, 40) == 42
    assert mathtools.least_multiple_greater_equal(7, 41) == 42
