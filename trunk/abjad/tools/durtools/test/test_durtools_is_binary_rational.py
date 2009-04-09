from abjad import *


def test_is_binary_rational_01( ):
   '''True when input is a Rational with denominator of the form 2**n.'''

   assert durtools.is_binary_rational(Rational(1, 1))
   assert durtools.is_binary_rational(Rational(1, 2))
   assert not durtools.is_binary_rational(Rational(1, 3))
   assert durtools.is_binary_rational(Rational(1, 4))
   assert not durtools.is_binary_rational(Rational(1, 5))
   assert not durtools.is_binary_rational(Rational(1, 6))
   assert not durtools.is_binary_rational(Rational(1, 7))
   assert durtools.is_binary_rational(Rational(1, 8))
   assert not durtools.is_binary_rational(Rational(1, 9))
   assert not durtools.is_binary_rational(Rational(1, 10))
   assert not durtools.is_binary_rational(Rational(1, 11))
   assert not durtools.is_binary_rational(Rational(1, 12))

