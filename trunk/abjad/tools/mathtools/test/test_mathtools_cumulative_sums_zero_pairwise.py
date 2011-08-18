from abjad import *
from abjad.tools import mathtools


def test_mathtools_cumulative_sums_zero_pairwise_01():
    '''Yield pairwise cumulative sums of l from 0.'''

    l = [3, 1, 2, 1, 3, 3, 1]
    g = mathtools.cumulative_sums_zero_pairwise(l)

    assert list(g) == [
        (0, 3), (3, 4), (4, 6), (6, 7), (7, 10), (10, 13), (13, 14)]


def test_mathtools_cumulative_sums_zero_pairwise_02():
    '''Yield pairwise cumulative sums of l from 0.'''

    l = [1, 2, 3, 4, 5, 6]
    g = mathtools.cumulative_sums_zero_pairwise(l)

    assert list(g) == [
        (0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]
