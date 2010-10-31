from abjad.tools.seqtools._group_sequence_elements_by_weights_exactly import \
   _group_sequence_elements_by_weights_exactly


def group_sequence_elements_once_by_weights_exactly_with_overhang(sequence, weights):
   '''Group `sequence` elements once by `weights` exactly with overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
      abjad> groups = seqtools.group_sequence_elements_once_by_weights_exactly_with_overhang(sequence, [3, 9])
      [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]


   Return list sequence element reference lists.
   '''

   return _group_sequence_elements_by_weights_exactly(
      sequence, weights, cyclic = False, overhang = True)
