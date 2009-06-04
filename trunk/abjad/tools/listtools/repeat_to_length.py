from __future__ import division
import math


def repeat_to_length(l, length):
   '''Repeat list ``l`` to ``length``.
   
   * ``l`` must be an iterable of one or more numbers.
   * ``length`` must be a nonnegative integer.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 11)
      [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

   When ``length < len(l)`` return only the first \
   ``length`` elements of ``l``.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 3)
      [0, 1, 2]

   When ``length`` is ``0`` return an empty list.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 0)
      [ ]'''

   assert isinstance(l, list)
   assert isinstance(length, int)
   assert 0 <= length
   assert 0 < len(l)

   if length == 0:
      return [ ]

   if len(l) == length:
      return l[:]
   elif len(l) > length:
      return l[0:length]
   else:
      l = l * int(math.ceil(length / len(l)))
      return l[0:length]
