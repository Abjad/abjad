from __future__ import division

def divide(total, parts):
   '''
   Divide a scalar total (int, float or rational) into the proportions given
   by the numbers in parts.
   Example:
   >>>  divide(Rational(1, 2), [1,1,3]) returns
   [Rational(1, 10), Rational(1, 10), Rational(3, 10)]
   '''
   return [total * p / sum(parts) for p in parts]

