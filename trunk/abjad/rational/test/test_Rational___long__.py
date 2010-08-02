from abjad import *


def test_rational_long_01( ):
   '''Rational numbers may have long numerators and denominators.'''

   p = Rational(1234567, 12345678)
   q = Rational(12345678, 123456789)

   assert not p == q
   assert p != q
   assert p <  q
   assert p <= q
   assert q >  p
   assert q >= p
