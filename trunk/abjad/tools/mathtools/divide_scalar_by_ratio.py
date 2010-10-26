from __future__ import division
from fractions import Fraction
from numbers import Number


def divide_scalar_by_ratio(scalar, ratio):
   '''Divide integer `scalar` by `ratio`::

      abjad> mathtools.divide_scalar_by_ratio(1, [1, 1, 3])
      [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

   Divide fraction `scalar` by `ratio`::

      abjad> mathtools.divide_scalar_by_ratio(Fraction(1), [1, 1, 3])
      [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

   Divide float `scalar` by ratio::

      abjad> mathtools.divide_scalar_by_ratio(1.0, [1, 1, 3])
      [0.20000000000000001, 0.20000000000000001, 0.60000000000000009]

   Raise type error on nonnumeric `scalar`.

   Raise type error on noninteger in `ratio`.

   Return list of fractions or list of floats.
   '''

   if not isinstance(scalar, Number):
      raise TypeError('scalar "%s" be number.' % str(scalar))

   if not all([isinstance(part, int) for part in ratio]):
      raise TypeError('ratio "%s" must comprise only integers.' % str(ratio))
  
   try:
      factor = Fraction(scalar, sum(ratio))
   except TypeError:
      factor = scalar / sum(ratio)

   return [p * factor for p in ratio]
