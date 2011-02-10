from abjad.tools.mathtools.cumulative_sums import cumulative_sums


def partition_integer_by_ratio(n, ratio):
   '''Partition integer `n` by `ratio`::


      abjad> mathtools.partition_integer_by_ratio(10, [1])
      [10]

   ::

      abjad> mathtools.partition_integer_by_ratio(10, [1, 1])
      [5, 5]

   ::

      abjad> mathtools.partition_integer_by_ratio(10, [1, 1, 1])
      [3, 4, 3]

   ::

      abjad> mathtools.partition_integer_by_ratio(10, [1, 1, 1, 1])
      [3, 2, 3, 2]

   ::

      abjad> mathtools.partition_integer_by_ratio(10, [1, 1, 1, 1, 1])
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

   Parts of sum to `n` with proportions equal to `ratio`
   with some rounding magic.

   Raise type error on noninteger `n`::

      abjad> mathtools.partition_integer_by_ratio('foo', [1, 1, 3])
      TypeError

   Raise value error on nonpositive `n`::

      abjad> mathtools.partition_integer_by_ratio(-1, [1, 1, 3])
      ValueError

   Return list of positive integers.
   '''

   if not isinstance(n, (int, long)):
      raise TypeError

   if n <= 0:
      raise ValueError

   assert all([isinstance(part, (int, long)) for part in ratio])

   result = [0]

   divisions = [float(n) * part / sum(ratio) for part in ratio]
   cumulative_divisions = cumulative_sums(divisions)

   for division in cumulative_divisions:
      rounded_division = int(round(division)) - sum(result)
      result.append(rounded_division)

   result = result[1:]

   return result
