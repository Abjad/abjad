from abjad import *


def test_interpolate_linear_01( ):
   x = interpolate.linear(0, 1, .5)
   assert x
