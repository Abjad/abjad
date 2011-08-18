from abjad import *
from abjad.tools import mathtools


def test_mathtools_difference_series_01():
    '''Return generator of differences l_i+1 - l_i for l_i in list l.'''

    t = [1, 1, 2, 3, 5, 5, 6]
    d = mathtools.difference_series(t)
    assert list(d) == [0, 1, 1, 2, 0, 1]
