from abjad import *


def test_durtools_positive_integer_to_implied_prolation_multipler_01( ):
   '''Return the prolation that positive integer denominator carries.'''

   assert durtools.positive_integer_to_implied_prolation_multipler(1) == Rational(1)
   assert durtools.positive_integer_to_implied_prolation_multipler(2) == Rational(1)
   assert durtools.positive_integer_to_implied_prolation_multipler(3) == Rational(2, 3)
   assert durtools.positive_integer_to_implied_prolation_multipler(4) == Rational(1)
   assert durtools.positive_integer_to_implied_prolation_multipler(5) == Rational(4, 5)
   assert durtools.positive_integer_to_implied_prolation_multipler(6) == Rational(2, 3)
   assert durtools.positive_integer_to_implied_prolation_multipler(7) == Rational(4, 7)
   assert durtools.positive_integer_to_implied_prolation_multipler(8) == Rational(1)
   assert durtools.positive_integer_to_implied_prolation_multipler(9) == Rational(8, 9)
   assert durtools.positive_integer_to_implied_prolation_multipler(10) == Rational(4, 5)
   assert durtools.positive_integer_to_implied_prolation_multipler(11) == Rational(8, 11)
   assert durtools.positive_integer_to_implied_prolation_multipler(12) == Rational(2, 3)
