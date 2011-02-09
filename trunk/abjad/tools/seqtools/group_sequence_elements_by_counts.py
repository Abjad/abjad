from abjad.tools.seqtools._partition_sequence_by_counts import _partition_sequence_by_counts


def group_sequence_elements_by_counts(sequence, counts, cyclic = False, overhang = False):
   '''.. versionadded:: 1.1.2

   Group `sequence` elements by `counts`::

      abjad> seqtools.group_sequence_elements_by_counts(range(10), [3, 4])
      [[0, 1, 2], [3, 4, 5, 6]]

   Return list of lists.
   '''

   return _partition_sequence_by_counts(
      sequence, counts, cyclic = cyclic, overhang = overhang, copy_elements = False)
