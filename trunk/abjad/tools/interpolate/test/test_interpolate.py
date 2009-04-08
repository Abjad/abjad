from abjad import *


def test_interpolate_cosine_01( ):
   x = interpolate.cosine(0, 1, .5)
   assert x


def test_interpolate_linear_01( ):
   x = interpolate.linear(0, 1, .5)
   assert x


def test_interpolate_exponential_01( ):
   x = interpolate.exponential(0, 1, .5, 4)
   assert x
