from abjad.tools.seqtools._group_sequence_elements_by_weights_exactly import \
   _group_sequence_elements_by_weights_exactly


def partition_sequence_cyclically_by_weights_exactly_without_overhang(sequence, weights):
   '''.. versionadded:: 1.1.1

   Partition `sequence` elements cyclically by `weights` exactly without overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
      abjad> groups = seqtools.partition_sequence_cyclically_by_weights_exactly_without_overhang(sequence, [12])
      [[3, 3, 3, 3], [4, 4, 4]]

   Return list of sequence element reference lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_sequence_elements_cyclically_by_weights_exactly_without_overhang( )`` to
      ``seqtools.partition_sequence_cyclically_by_weights_exactly_without_overhang( )``.
   '''

   return _group_sequence_elements_by_weights_exactly(
      sequence, weights, cyclic = True, overhang = False)
