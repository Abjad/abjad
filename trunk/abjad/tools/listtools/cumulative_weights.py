from abjad.rational.rational import Rational
from abjad.tools import mathtools


def cumulative_weights(l):
   '''Yield weights of the cumulative elements in *l*

   .. note:: This function returns a generator.

   ::

      abjad> l = [1, -2, -3, 4, -5, -6, 7, -8, -9, 10]
      abjad> list(listtools.cumulative_weights(l))
      [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]

   ::

      abjad> l = [-1, -2, -3, -4, -5, 6, 7, 8, 9, 10]
      abjad> list(listtools.cumulative_weights(l))
      [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]

   ::

      abjad> l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      abjad> list(listtools.cumulative_weights(l))
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

   ::

      abjad> l = [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
      abjad> list(listtools.cumulative_weights(l))
      [1, 3, 6, 10, 15, 15, 15, 15, 15, 15]

   ::

      abjad> l = [-1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
      abjad> list(listtools.cumulative_weights(l))
      [1, 3, 6, 10, 15, 15, 15, 15, 15, 15]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> list(listtools.cumulative_weights('foo'))
      TypeError
   '''

   if not isinstance(l, list):
      raise TypeError

   if not all([isinstance(x, (int, long, float, Rational)) for x in l]):
      raise ValueError

   total_weight = 0

   for x in l:
      total_weight = total_weight + abs(x)
      yield total_weight

   raise StopIteration
