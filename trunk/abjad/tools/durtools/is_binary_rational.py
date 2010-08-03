from abjad.Rational import Rational
import math


def is_binary_rational(rational):
   '''True when `rational` is of the form ``1/2**n``.

   Otherwise false. ::

      abjad> for n in range(1, 17):
      ...     rational = Rational(1, n)
      ...     print '%s\\t%s' % (rational, durtools.is_binary_rational(rational))
      ... 
      1       True
      1/2     True
      1/3     False
      1/4     True
      1/5     False
      1/6     False
      1/7     False
      1/8     True
      1/9     False
      1/10    False
      1/11    False
      1/12    False
      1/13    False
      1/14    False
      1/15    False
      1/16    True
   '''

   assert isinstance(rational, Rational)
   exponent = math.log(rational._d, 2)
   return int(exponent) == exponent
