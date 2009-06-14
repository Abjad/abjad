from abjad.rational import Rational
import math


def is_binary_rational(rational):
   '''True when rational is of the form 1/2**n, otherwise False.

      for i in range(1, 12 + 1):
         print Rational(1, i), _is_binary(Rational(1, i))

      1 True
      1/2 True
      1/3 False
      1/4 True
      1/5 False
      1/6 False
      1/7 False
      1/8 True
      1/9 False
      1/10 False
      1/11 False
      1/12 False'''

   assert isinstance(rational, Rational)
   exponent = math.log(rational._d, 2)
   return int(exponent) == exponent
