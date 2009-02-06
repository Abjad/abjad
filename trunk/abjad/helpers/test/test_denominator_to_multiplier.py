from abjad import *
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier


def test_denominator_to_multiplier_01( ):
   '''Return the prolation that positive integer denominator carries.'''

   assert _denominator_to_multiplier(1) == Rational(1)
   assert _denominator_to_multiplier(2) == Rational(1)
   assert _denominator_to_multiplier(3) == Rational(2, 3)
   assert _denominator_to_multiplier(4) == Rational(1)
   assert _denominator_to_multiplier(5) == Rational(4, 5)
   assert _denominator_to_multiplier(6) == Rational(2, 3)
   assert _denominator_to_multiplier(7) == Rational(4, 7)
   assert _denominator_to_multiplier(8) == Rational(1)
   assert _denominator_to_multiplier(9) == Rational(8, 9)
   assert _denominator_to_multiplier(10) == Rational(4, 5)
   assert _denominator_to_multiplier(11) == Rational(8, 11)
   assert _denominator_to_multiplier(12) == Rational(2, 3)
