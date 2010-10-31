from abjad import *


def test_seqtools_split_sequence_once_by_weights_without_overhang_01( ):

   sequence = (10, -10, 10, -10)
   pieces = seqtools.split_sequence_once_by_weights_without_overhang(sequence, [3, 15, 3])
   assert pieces == [(3, ), (7, -8), (-2, 1)]
