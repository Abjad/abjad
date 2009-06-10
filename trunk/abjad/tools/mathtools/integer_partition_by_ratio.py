from abjad.tools.mathtools.sums import sums as mathtools_sums


def integer_partition_by_ratio(n, ratio):
   '''Partition integer ``n`` into parts such that the sum \
   of all parts in parts equals ``n`` and such that the proportions \
   between the parts in parts equals the the proportions in ``ratio`` \
   with some rounding magic.

   ::

      abjad> mathtools.integer_partition_by_ratio(10, [1])
      [10]

   ::

      abjad> mathtools.integer_partition_by_ratio(10, [1, 1])
      [5, 5]

   ::

      abjad> mathtools.integer_partition_by_ratio(10, [1, 1, 1])
      [3, 4, 3]

   ::

      abjad> mathtools.integer_partition_by_ratio(10, [1, 1, 1, 1])
      [3, 2, 3, 2]

   ::

      abjad> mathtools.integer_partition_by_ratio(10, [1, 1, 1, 1, 1])
      [2, 2, 2, 2, 2]
      
   ::

      abjad> ratio(10, [1, 2])
      [3, 7]

   ::

      abjad> ratio(10, [3, 1])
      [8, 2]

   ::

      abjad> ratio(10, [3, 2])
      [6, 4]


   Raise :exc:`TypeError` on noninteger *n*::

      abjad> mathtools.integer_partition_by_ratio('foo', [1, 1, 3])
      TypeError

   Raise :exc:`ValueError` on nonpositive *n*::

      abjad> mathtools.integer_partition_by_ratio(-1, [1, 1, 3])
      ValueError'''

   if not isinstance(n, (int, long)):
      raise TypeError

   if n <= 0:
      raise ValueError

   assert all([isinstance(part, (int, long)) for part in ratio])

   result = [0]

   divisions = [float(n) * part / sum(ratio) for part in ratio]
   cumulative_divisions = mathtools_sums(divisions)

   for division in cumulative_divisions:
      rounded_division = int(round(division)) - sum(result)
      result.append(rounded_division)

   result = result[1:]

   return result
