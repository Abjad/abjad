from abjad import *
from abjad.tools import durtools


def test_durtools_duration_token_to_rational_01( ):

   assert durtools.duration_token_to_rational((4, 16)) == Fraction(1, 4)
   assert durtools.duration_token_to_rational((1, 4)) == Fraction(1, 4)
   assert durtools.duration_token_to_rational('4') == Fraction(1, 4)
   assert durtools.duration_token_to_rational('8.') == Fraction(3, 16)
   assert durtools.duration_token_to_rational(1) == Fraction(1)
