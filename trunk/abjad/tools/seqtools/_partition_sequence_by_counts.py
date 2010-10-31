from abjad.tools.seqtools.all_are_nonnegative_integers import all_are_nonnegative_integers
from abjad.tools.seqtools.pairwise_cumulative_sums_zero import pairwise_cumulative_sums_zero
from abjad.tools.seqtools.repeat_sequence_to_weight import repeat_sequence_to_weight
from abjad.tools import mathtools
import copy


## TODO: renamed 'lengths' to 'counts' ##
def _partition_sequence_by_counts(sequence, lengths, cyclic = False, overhang = False, copy_elements = True):
   '''Partition `sequence` by `lengths`::

      abjad> seqtools._partition_list_by_counts(range(10), [3])
      [[0, 1, 2]]

   When ``cyclic = True`` repeat the elements in `lengths`::

      abjad> seqtools._partition_list_by_counts(range(10), [3], cyclic = True) 
      [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

   When ``overhang = True`` return any remaining unicorporated
   elements of `sequence` as a final part in ``result``::

      abjad> seqtools._partition_list_by_counts(range(10), [3], overhang = True)
      [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   When both ``cyclic = True`` and ``overhang = True`` repeat the 
   elements in `lengths` and return any remaining unincorporated 
   elements of `l` as a final part in ``result``::

      abjad> seqtools._partition_list_by_counts(range(10), [3], cyclic = True, overhang = True)
      [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

   Examples with ``1 < len(lengths)``::

      abjad> seqtools._partition_list_by_counts(range(16), [4, 3])
      [[0, 1, 2, 3], [4, 5, 6]]

   ::

      abjad> seqtools._partition_list_by_counts(range(16), [4, 3], cyclic = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

   ::

      abjad> seqtools._partition_list_by_counts(range(16), [4, 3], overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

   ::

      abjad> seqtools._partition_list_by_counts(range(16), [4, 3], cyclic = True, overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]

   Return list of `sequence` types.
   '''

   ## TODO: Document zero-length boundary case with examples and tests ##
   assert all_are_nonnegative_integers(lengths)

   result = [ ]

   if cyclic == True:
      if overhang == True:
         lengths = repeat_sequence_to_weight(lengths, len(sequence))
      else:
         lengths = repeat_sequence_to_weight(lengths, len(sequence), remainder = 'less')
   elif overhang == True:
      weight_lengths = mathtools.weight(lengths)
      len_sequence = len(sequence)
      if weight_lengths < len_sequence:
         lengths.append(len(sequence) - weight_lengths)

   for start, stop in pairwise_cumulative_sums_zero(lengths):
      if copy_elements:
         part = [ ]
         for element in sequence[start:stop]:
            part.append(copy.copy(element))
         part = type(sequence)(part)
         result.append(part)
      else:
         result.append(sequence[start:stop])

   return result
