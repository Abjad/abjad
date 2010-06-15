from abjad import *


def test_durtools_integer_denominator_to_implied_prolation_01( ):
   '''Return the prolation that positive integer denominator carries.'''

   assert durtools.integer_denominator_to_implied_prolation(1) == Rational(1)
   assert durtools.integer_denominator_to_implied_prolation(2) == Rational(1)
   assert durtools.integer_denominator_to_implied_prolation(3) == Rational(2, 3)
   assert durtools.integer_denominator_to_implied_prolation(4) == Rational(1)
   assert durtools.integer_denominator_to_implied_prolation(5) == Rational(4, 5)
   assert durtools.integer_denominator_to_implied_prolation(6) == Rational(2, 3)
   assert durtools.integer_denominator_to_implied_prolation(7) == Rational(4, 7)
   assert durtools.integer_denominator_to_implied_prolation(8) == Rational(1)
   assert durtools.integer_denominator_to_implied_prolation(9) == Rational(8, 9)
   assert durtools.integer_denominator_to_implied_prolation(10) == Rational(4, 5)
   assert durtools.integer_denominator_to_implied_prolation(11) == Rational(8, 11)
   assert durtools.integer_denominator_to_implied_prolation(12) == Rational(2, 3)
