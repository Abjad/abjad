from abjad import *


def test_seqtools_group_sequence_elements_once_by_weights_exactly_with_overhang_01( ):

   sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
   groups = seqtools.group_sequence_elements_once_by_weights_exactly_with_overhang(
      sequence, [3, 9])
   assert groups == [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]
