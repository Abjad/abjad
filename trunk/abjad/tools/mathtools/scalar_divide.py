from __future__ import division


def scalar_divide(total, parts):
   '''Divide a scalar total (int, float or rational) into 
      proportions given by numbers in parts.

      Example:

      >>>  divide(Rational(1, 2), [1,1,3]) returns
      [Rational(1, 10), Rational(1, 10), Rational(3, 10)]'''

   return [total * p / sum(parts) for p in parts]
