from abjad import *


def test_seqtools_group_sequence_elements_by_sign_01( ):

   sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   groups = seqtools.group_sequence_elements_by_sign(sequence)
   assert groups == [(0, 0), (-1, -1), (2, 3), (-5,), (1, 2, 5), (-5, -6)]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1])
   assert groups == [0, 0, (-1, -1), 2, 3, (-5,), 1, 2, 5, (-5, -6)]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [0])
   assert groups == [(0, 0), -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [1])
   assert groups == [0, 0, -1, -1, (2, 3), -5, (1, 2, 5), -5, -6]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1, 0])
   assert groups == [(0, 0), (-1, -1), 2, 3, (-5,), 1, 2, 5, (-5, -6)]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1, 1])
   assert groups == [0, 0, (-1, -1), (2, 3), (-5,), (1, 2, 5), (-5, -6)]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [0, 1])
   assert groups == [(0, 0), -1, -1, (2, 3), -5, (1, 2, 5), -5, -6]

   groups = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1, 0, 1])
   assert groups == [(0, 0), (-1, -1), (2, 3), (-5,), (1, 2, 5), (-5, -6)]   
