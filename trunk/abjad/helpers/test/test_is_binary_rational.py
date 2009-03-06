from abjad.helpers.is_binary_rational import _is_binary_rational
from abjad import *


def test_is_binary_rational_01( ):
   '''True when input is a Rational with denominator of the form 2**n.'''

   assert _is_binary_rational(Rational(1, 1))
   assert _is_binary_rational(Rational(1, 2))
   assert not _is_binary_rational(Rational(1, 3))
   assert _is_binary_rational(Rational(1, 4))
   assert not _is_binary_rational(Rational(1, 5))
   assert not _is_binary_rational(Rational(1, 6))
   assert not _is_binary_rational(Rational(1, 7))
   assert _is_binary_rational(Rational(1, 8))
   assert not _is_binary_rational(Rational(1, 9))
   assert not _is_binary_rational(Rational(1, 10))
   assert not _is_binary_rational(Rational(1, 11))
   assert not _is_binary_rational(Rational(1, 12))

