from abjad.rational.rational import Rational
from abjad.helpers.closest_rational_with_denominator import _closest_rational_with_denominator

def test_closest_rational_with_denominator_01( ):
   '''
   By default the function returns a Rational smaller than the one given.
   '''
   rational, residue = _closest_rational_with_denominator(Rational(3, 7), 8)
   assert rational == Rational(3, 8)
   assert residue == Rational(3, 7) - Rational(3, 8)


def test_closest_rational_with_denominator_02( ):
   '''
   Set direction to 'above' to get a Rational > than that given.
   '''
   rational, residue = _closest_rational_with_denominator(Rational(3, 7), 8,
      direction = 'above')
   assert rational == Rational(4, 8)
   assert residue == Rational(3, 7) - Rational(4, 8)

