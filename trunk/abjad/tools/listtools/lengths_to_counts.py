from abjad.tools import mathtools


def lengths_to_counts(l):
   '''Return list of counts from list *l* of lengths.

   .. note:: Counting starts at ``1``.

   ::

      abjad> listtools.lengths_to_counts([1, 2, -3, -4, 5])
      [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]

   ::

      abjad> listtools.lengths_to_counts([1, 0, -3, -4, 5])
      [[1], [ ], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]
   '''

   if not isinstance(l, list):
      raise TypeError

   if not all([isinstance(x, (int, long)) for x in l]):
      raise ValueError

   result = [ ]
   cur = 1

   for length in l:
      abs_length = abs(length)
      part = range(cur, cur + abs_length)
      part = [mathtools.sign(length) * x for x in part]
      result.append(part)
      cur += abs_length

   return result
