from __future__ import division
from abjad.rational.rational import Rational


def divide_scalar_by_ratio(scalar, ratio):
   '''Divide *scalar* proportionally by *ratio*.
   Return list of ``len(ratio)`` parts.

   ::

      abjad> mathtools.divide_scalar_by_ratio(Rational(1, 2), [1, 1, 3])
      [Rational(1, 10), Rational(1, 10), Rational(3, 10)]

   ::

      abjad> mathtools.divide_scalar_by_ratio(1, [1, 1, 3])
      [0.20000000000000001, 0.20000000000000001, 0.59999999999999998]

   Raise :exc:`TypeError` on nonnumeric *scalar*::

      abjad> mathtools.divide_scalar_by_ratio('foo', [1, 1, 3])
      TypeError

   .. todo:: Do we want ``mathtools.divide_scalar_by_ratio(1, [1, 1, 3])`` to \
      return rational values instead of floats?'''

   if not isinstance(scalar, (int, float, long, Rational)):
      raise TypeError

   return [scalar * p / sum(ratio) for p in ratio]
