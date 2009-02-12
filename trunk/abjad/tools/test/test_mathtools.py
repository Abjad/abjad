from abjad.tools import mathtools

def test_mathtools_interpolate_cosine_01( ):
   x = mathtools.interpolate_cosine(0, 1, .5)
   assert x


def test_mathtools_interpolate_linear_01( ):
   x = mathtools.interpolate_linear(0, 1, .5)
   assert x


def test_mathtools_interpolate_exponential_01( ):
   x = mathtools.interpolate_exponential(0, 1, .5, 4)
   assert x

