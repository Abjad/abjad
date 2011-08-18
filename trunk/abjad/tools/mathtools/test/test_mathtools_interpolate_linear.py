from abjad import *
from abjad.tools import mathtools


def test_mathtools_interpolate_linear_01():
    x = mathtools.interpolate_linear(0, 1, .5)
    assert x
