from abjad.tools import mathtools


def lengths_to_counts(sequence):
   '''Interpret `sequence` elements as lengths and construct list of count sublists::

      abjad> seqtools.lengths_to_counts([1, 2, -3, -4, 5])
      [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]

   ::

      abjad> seqtools.lengths_to_counts([1, 0, -3, -4, 5])
      [[1], [ ], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]

   Note that counting starts at ``1``.

   Return newly constructed list of lists.
   '''

   if not isinstance(sequence, list):
      raise TypeError

   if not all([isinstance(x, (int, long)) for x in sequence]):
      raise ValueError

   result = [ ]
   cur = 1

   for length in sequence:
      abs_length = abs(length)
      part = range(cur, cur + abs_length)
      part = [mathtools.sign(length) * x for x in part]
      result.append(part)
      cur += abs_length

   return result
