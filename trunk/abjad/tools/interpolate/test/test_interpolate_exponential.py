from abjad import *


def test_interpolate_exponential_01( ):
   x = interpolate.exponential(0, 1, .5, 4)
   assert x
