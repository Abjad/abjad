from abjad import *


def test_interpolate_cosine_01( ):
   x = interpolate.cosine(0, 1, .5)
   assert x
