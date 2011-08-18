from abjad import *
from abjad.tools import mathtools


def test_mathtools_interpolate_exponential_01():
    x = mathtools.interpolate_exponential(0, 1, .5, 4)
    assert x
