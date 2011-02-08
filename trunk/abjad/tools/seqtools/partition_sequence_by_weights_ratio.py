from fractions import Fraction
from abjad.tools import mathtools
from abjad.tools.mathtools.cumulative_sums import cumulative_sums
from abjad.tools.seqtools.flatten_sequence import flatten_sequence
from abjad.tools.mathtools.weight import weight


def partition_sequence_by_weights_ratio(sequence, ratio):
   '''.. versionadded:: 1.1.2

   Partition `sequence` into disjunct parts such that propotions of 
   the weights of the parts equal the proportions in `ratio`
   with some rounding magic::

      abjad> seqtools.partition_sequence_by_weights_ratio([1] * 10, [1, 1, 1])
      [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

   ::

      abjad> seqtools.partition_sequence_by_weights_ratio([1] * 10, [1, 1, 1, 1])
      [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

   ::

      abjad> seqtools.partition_sequence_by_weights_ratio([1] * 10, [2, 2, 3])
      [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

   ::

      abjad> seqtools.partition_sequence_by_weights_ratio([1] * 10, [3, 2, 2])
      [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1]]

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_sequence_by_weights_ratio( )`` to
      ``seqtools.partition_sequence_by_weights_ratio( )``.
   '''

   list_weight = weight(sequence)
   weights = mathtools.partition_integer_by_ratio(list_weight, ratio)
   cumulative_weights = cumulative_sums(weights)

   result = [ ]
   sublist = [ ]
   result.append(sublist)
   cur_cumulative_weight = cumulative_weights.pop(0)
   for n in sequence:
      if not isinstance(n, (int, long, float, Fraction)):
         raise TypeError('must be number.')
      sublist.append(n)
      while cur_cumulative_weight <= weight(flatten_sequence(result)):
         try:
            cur_cumulative_weight = cumulative_weights.pop(0)
            sublist = [ ]
            result.append(sublist)
         except IndexError:
            break

   return result
