from abjad.tools.seqtools._group_sequence_elements_by_weights_at_most import \
   _group_sequence_elements_by_weights_at_most


def partition_sequence_cyclically_by_weights_at_most_without_overhang(sequence, weights):
   '''Group `sequence` elements cyclically by `weights` at most without overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
      abjad> groups = seqtools.partition_sequence_cyclically_by_weights_at_most_without_overhang(sequence, [10, 5])
      [[3, 3, 3], [3], [4, 4], [4]]

   Return list sequence element reference lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_sequence_elements_cyclically_by_weights_at_most_without_overhang( )`` to
      ``seqtools.partition_sequence_cyclically_by_weights_at_most_without_overhang( )``.
   '''

   return _group_sequence_elements_by_weights_at_most(
      sequence, weights, cyclic = True, overhang = False)
