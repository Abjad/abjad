from __future__ import division
from abjad.rational.rational import Rational


def scalar_divide(total, parts):
   '''Divide scalar *total* proportionally by *parts*.

   ::

      abjad> mathtools.scalar_divide(Rational(1, 2), [1, 1, 3])
      [Rational(1, 10), Rational(1, 10), Rational(3, 10)]

   ::

      abjad> mathtools.scalar_divide(1, [1, 1, 3])
      [0.20000000000000001, 0.20000000000000001, 0.59999999999999998]

   Raise :exc:`TypeError` on nonnumeric *total*::

      abjad> mathtools.scalar_divide('foo', [1, 1, 3])
      TypeError

   .. todo:: Do we want ``mathtools.scalar_divide(1, [1, 1, 3])`` to \
      return rational values instead of floats?'''

   if not isinstance(total, (int, float, long, Rational)):
      raise TypeError

   return [total * p / sum(parts) for p in parts]
