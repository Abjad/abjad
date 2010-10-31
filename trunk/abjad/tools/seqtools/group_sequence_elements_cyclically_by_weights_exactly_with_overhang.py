from abjad.tools.seqtools._group_sequence_elements_by_weights_exactly import \
   _group_sequence_elements_by_weights_exactly


def group_sequence_elements_cyclically_by_weights_exactly_with_overhang(sequence, weights):
   '''Group `sequence` elements cyclically by `weights` exactly with overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
      abjad> groups = seqtools.group_sequence_elements_cyclically_by_weights_exactly_with_overhang(sequence, [12])
      [[3, 3, 3, 3], [4, 4, 4], [4, 5]]

   Return list of sequence element reference lists.
   '''

   return _group_sequence_elements_by_weights_exactly(
      sequence, weights, cyclic = True, overhang = True)
