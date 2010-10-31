from abjad import *


def test_seqtools_group_sequence_elements_once_by_weights_at_most_without_overhang_01( ):

   sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
   groups = seqtools.group_sequence_elements_once_by_weights_at_most_without_overhang(
      sequence, [10, 4])
   assert groups == [[3, 3, 3], [3]]
