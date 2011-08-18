from abjad import *
from abjad.tools import mathtools


def test_mathtools_least_common_multiple_01():
    '''Works with two positive integers.'''

    assert mathtools.least_common_multiple(4, 4) == 4
    assert mathtools.least_common_multiple(4, 5) == 20
    assert mathtools.least_common_multiple(4, 6) == 12
    assert mathtools.least_common_multiple(4, 7) == 28
    assert mathtools.least_common_multiple(4, 8) == 8
    assert mathtools.least_common_multiple(4, 9) == 36
    assert mathtools.least_common_multiple(4, 10) == 20
    assert mathtools.least_common_multiple(4, 11) == 44


def test_mathtools_least_common_multiple_02():
    '''Works with one positive integer.'''

    assert mathtools.least_common_multiple(1) == 1
    assert mathtools.least_common_multiple(2) == 2


def test_mathtools_least_common_multiple_03():
    '''Works with more than two positive integers.'''

    assert mathtools.least_common_multiple(2, 3, 4) == 12
    assert mathtools.least_common_multiple(2, 3, 4, 6, 12) == 12
    assert mathtools.least_common_multiple(2, 3, 4, 5, 6, 12) == 60
