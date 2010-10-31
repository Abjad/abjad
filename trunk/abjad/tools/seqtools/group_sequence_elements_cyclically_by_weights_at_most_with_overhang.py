from abjad.tools.seqtools._group_sequence_elements_by_weights_at_most import \
   _group_sequence_elements_by_weights_at_most


def group_sequence_elements_cyclically_by_weights_at_most_with_overhang(sequence, weights):
   '''Group `sequence` elements cyclically by `weights` at most with overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
      abjad> groups = seqtools.group_sequence_elements_cyclically_by_weights_at_most_with_overhang(sequence, [10, 5])
      [[3, 3, 3], [3], [4, 4], [4], [4, 5], [5]]

   Return list sequence element reference lists.
   '''

   return _group_sequence_elements_by_weights_at_most(
      sequence, weights, cyclic = True, overhang = True)
