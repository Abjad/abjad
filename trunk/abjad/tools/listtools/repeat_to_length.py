from __future__ import division
import math


def repeat_to_length(l, length, start_index = 0):
   '''Repeat list *l* to nonnegative integer *length*.
   
   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 11)
      [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

   When *length < len(l)* return ``l[:length]``.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 3)
      [0, 1, 2]

   When ``length = 0`` return an empty list.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 0)
      [ ]

   Read optional integer *start_index* modulo the length of *l*.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 10, 2)
      [2, 3, 4, 0, 1, 2, 3, 4, 0, 1]

   ::

      abjad> listtools.repeat_to_length(range(5), 10, -99)
      [1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

   ::

      abjad> listtools.repeat_to_length(range(5), 10, 99)
      [4, 0, 1, 2, 3, 4, 0, 1, 2, 3]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> listtools.repeat_to_length('foo', 10)
      TypeError
   '''

   if not isinstance(l, list):
      raise TypeError

   if not isinstance(length, (int, long)):
      raise TypeError

   if length < 0:
      raise ValueError

   if len(l) <= 0:
      raise ValueError

   start_index %= len(l)
   stop_index = start_index + length
   l = l * int(math.ceil(stop_index / len(l)))

   return l[start_index:stop_index]
