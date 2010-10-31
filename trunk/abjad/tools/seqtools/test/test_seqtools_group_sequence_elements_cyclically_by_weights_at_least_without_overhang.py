from abjad import *


def test_seqtools_group_sequence_elements_cyclically_by_weights_at_least_without_overhang_01( ):

   sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
   groups = seqtools.group_sequence_elements_cyclically_by_weights_at_least_without_overhang(
      sequence, [10, 4])
   assert groups == [[3, 3, 3, 3], [4], [4, 4, 4], [5]]
