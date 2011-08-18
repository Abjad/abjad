from abjad import *
from abjad.tools import mathtools


def test_mathtools_greatest_multiple_less_equal_01():
    '''Return the least multiple of m greater than or equal to n.'''

    assert mathtools.greatest_multiple_less_equal(10, 0) == 0
    assert mathtools.greatest_multiple_less_equal(10, 1) == 0
    assert mathtools.greatest_multiple_less_equal(10, 2) == 0
    assert mathtools.greatest_multiple_less_equal(10, 13) == 10
    assert mathtools.greatest_multiple_less_equal(10, 28) == 20
    assert mathtools.greatest_multiple_less_equal(10, 40) == 40
    assert mathtools.greatest_multiple_less_equal(10, 41) == 40


def test_mathtools_greatest_multiple_less_equal_02():
    '''Return the least multiple of m greater than or equal to n.'''

    assert mathtools.greatest_multiple_less_equal(7, 0) == 0
    assert mathtools.greatest_multiple_less_equal(7, 1) == 0
    assert mathtools.greatest_multiple_less_equal(7, 2) == 0
    assert mathtools.greatest_multiple_less_equal(7, 13) == 7
    assert mathtools.greatest_multiple_less_equal(7, 28) == 28
    assert mathtools.greatest_multiple_less_equal(7, 40) == 35
    assert mathtools.greatest_multiple_less_equal(7, 41) == 35
