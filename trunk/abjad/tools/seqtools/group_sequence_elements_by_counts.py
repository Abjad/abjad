from abjad.tools.seqtools._partition_sequence_by_counts import _partition_sequence_by_counts


def group_sequence_elements_by_counts(sequence, lengths, cyclic = False, overhang = False):
   '''.. versionadded:: 1.1.2

   Docs.
   '''

   return _partition_sequence_by_counts(
      sequence, lengths, cyclic = cyclic, overhang = overhang, copy_elements = False)
