from abjad import *


def test_mathtools_interpolate_cosine_01( ):
   x = mathtools.interpolate_cosine(0, 1, .5)
   assert x
