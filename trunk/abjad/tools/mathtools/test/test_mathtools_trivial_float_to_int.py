from abjad import *


def test_mathtools_trivial_float_to_int_01( ):

   i = mathtools.trivial_float_to_int(-7.0)
   assert isinstance(i, int)
   assert i == -7

   i = mathtools.trivial_float_to_int(0.0)
   assert isinstance(i, int)
   assert i == 0

   i = mathtools.trivial_float_to_int(7.0)
   assert isinstance(i, int)
   assert i == 7


def test_mathtools_trivial_float_to_int_02( ):

   i = mathtools.trivial_float_to_int(-7.5)
   assert not isinstance(i, int)
   assert i == -7.5

   i = mathtools.trivial_float_to_int(0.5)
   assert not isinstance(i, int)
   assert i == 0.5

   i = mathtools.trivial_float_to_int(7.5)
   assert not isinstance(i, int)
   assert i == 7.5
