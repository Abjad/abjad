from abjad import *


def test_tuplettools_is_proper_tuplet_multiplier_01( ):
   '''True when multiplier is a rational strictly greater than 1/2
      and strictly less than 2.'''

   assert not tuplettools.is_proper_tuplet_multiplier(Rational(1, 10))
   assert not tuplettools.is_proper_tuplet_multiplier(Rational(2, 10))
   assert not tuplettools.is_proper_tuplet_multiplier(Rational(3, 10))
   assert not tuplettools.is_proper_tuplet_multiplier(Rational(4, 10))
   assert not tuplettools.is_proper_tuplet_multiplier(Rational(5, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(6, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(7, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(8, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(9, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(10, 10))


def test_tuplettools_is_proper_tuplet_multiplier_02( ):
   '''True when multiplier is a rational strictly greater than 1/2
      and strictly less than 2.'''

   assert tuplettools.is_proper_tuplet_multiplier(Rational(11, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(12, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(13, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(14, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(15, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(16, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(17, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(18, 10))
   assert tuplettools.is_proper_tuplet_multiplier(Rational(19, 10))
   assert not tuplettools.is_proper_tuplet_multiplier(Rational(20, 10))
