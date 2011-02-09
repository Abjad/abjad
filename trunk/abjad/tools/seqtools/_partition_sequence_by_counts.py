from abjad.tools.seqtools.all_are_nonnegative_integers import all_are_nonnegative_integers
from abjad.tools.seqtools.list_pairwise_cumulative_sums_from_zero import list_pairwise_cumulative_sums_from_zero
from abjad.tools.seqtools.repeat_sequence_to_weight_at_most import repeat_sequence_to_weight_at_most
from abjad.tools.seqtools.repeat_sequence_to_weight_exactly import repeat_sequence_to_weight_exactly
from abjad.tools import mathtools
import copy


def _partition_sequence_by_counts(sequence, counts, cyclic = False, overhang = False, 
   copy_elements = True):
   '''Partition sequence by count:

      abjad> seqtools._partition_sequence_by_counts(range(10), [3])
      [[0, 1, 2]]

   Partition sequence cyclically by count:

      abjad> seqtools._partition_sequence_by_counts(range(10), [3], cyclic = True) 
      [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

   Partition sequence by count with overhang:

      abjad> seqtools._partition_sequence_by_counts(range(10), [3], overhang = True)
      [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   Partition sequence cyclically by count with overhang:

      abjad> seqtools._partition_sequence_by_counts(range(10), [3], cyclic = True, overhang = True)
      [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

   Partition sequence once by counts:

      abjad> seqtools._partition_sequence_by_counts(range(16), [4, 3])
      [[0, 1, 2, 3], [4, 5, 6]]

   Partition sequence cyclically by counts:

      abjad> seqtools._partition_sequence_by_counts(range(16), [4, 3], cyclic = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

   Partition sequence by counts with overhang:

      abjad> seqtools._partition_sequence_by_counts(range(16), [4, 3], overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

   Partition sequence cyclically by counts with overhang:

      abjad> seqtools._partition_sequence_by_counts(
         range(16), [4, 3], cyclic = True, overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]

   Return list of sequence types.
   '''

   assert all_are_nonnegative_integers(counts)

   result = [ ]

   if cyclic == True:
      if overhang == True:
         counts = repeat_sequence_to_weight_exactly(counts, len(sequence))
      else:
         counts = repeat_sequence_to_weight_at_most(counts, len(sequence))
   elif overhang == True:
      weight_counts = mathtools.weight(counts)
      len_sequence = len(sequence)
      if weight_counts < len_sequence:
         counts = list(counts)
         counts.append(len(sequence) - weight_counts)

   for start, stop in list_pairwise_cumulative_sums_from_zero(counts):
      if copy_elements:
         part = [ ]
         for element in sequence[start:stop]:
            part.append(copy.copy(element))
         part = type(sequence)(part)
         result.append(part)
      else:
         result.append(sequence[start:stop])

   return result
