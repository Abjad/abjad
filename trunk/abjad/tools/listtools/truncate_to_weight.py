from abjad.tools import mathtools
from abjad.tools.listtools.weight import weight


def truncate_to_weight(l, total):
   '''Truncate list *l* such that ``listtools.weight(l) == total``.

   ::

      abjad> for x in range(10):
      ...     print x, listtools.truncate_to_weight([-2, 2, -2], x)
      ... 
      0 [ ]
      1 [-1]
      2 [-2]
      3 [-2, 1]
      4 [-2, 2]
      5 [-2, 2, -1]
      6 [-2, 2, -2]
      7 [-2, 2, -2]
      8 [-2, 2, -2]
      9 [-2, 2, -2]
   
   ::

      abjad> l = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
      abjad> for x in range(10):
      ...     print x, listtools.truncate_to_weight(l, x)
      ... 
      0 [ ]
      1 [-1]
      2 [-1, 1]
      3 [-1, 2]
      4 [-1, 2, -1]
      5 [-1, 2, -2]
      6 [-1, 2, -3]
      7 [-1, 2, -3, 1]
      8 [-1, 2, -3, 2]
      9 [-1, 2, -3, 3]

   Return empty list when ``total == 0``::

      abjad> listtools.truncate_to_weight([1, 2, 3, 4, 5], 0)
      [ ]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> listtools.truncate_to_weight('foo', 4)
      TypeError

   Raise :exc:`ValueError` on negative *total*::

      abjad> listtools.truncate_to_weight([2, 2, 2], -4)
      ValueError
   '''

   if not isinstance(l, list):
      raise TypeError

   if total < 0:
      raise ValueError

   result = [ ]

   if total == 0:
      return result

   accumulation = 0
   for x in l:
      accumulation += abs(x)
      if accumulation < total:
         result.append(x)
      else:
         sign = mathtools.sign(x)
         trimmed_part = total - weight(result)
         trimmed_part *= sign
         result.append(trimmed_part)
         break

   return result
