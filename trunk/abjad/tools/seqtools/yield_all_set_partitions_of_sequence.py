from abjad.tools.seqtools.generate_all_restricted_growth_functions_of_length import \
   generate_all_restricted_growth_functions_of_length
from abjad.tools.seqtools.partition_sequence_by_restricted_growth_function import \
   partition_sequence_by_restricted_growth_function


def yield_all_set_partitions_of_sequence(sequence):
   '''.. versionadded:: 1.1.2

   Yield all set partitions of `sequence` in restricted growth function order::

      abjad> for set_parition in seqtools.yield_all_set_partitions_of_sequence([21, 22, 23, 24]):
      ...     set_partition
      ... 
      [[21, 22, 23, 24]]
      [[21, 22, 23], [24]]
      [[21, 22, 24], [23]]
      [[21, 22], [23, 24]]
      [[21, 22], [23], [24]]
      [[21, 23, 24], [22]]
      [[21, 23], [22, 24]]
      [[21, 23], [22], [24]]
      [[21, 24], [22, 23]]
      [[21], [22, 23, 24]]
      [[21], [22, 23], [24]]
      [[21, 24], [22], [23]]
      [[21], [22, 24], [23]]
      [[21], [22], [23, 24]]
      [[21], [22], [23], [24]]

   Return generator of list of lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.all_set_partitions( )`` to
      ``seqtools.yield_all_set_partitions_of_sequence( )``.
   '''

   for rgf in generate_all_restricted_growth_functions_of_length(len(sequence)):
      partition = partition_sequence_by_restricted_growth_function(sequence, rgf)
      yield partition
