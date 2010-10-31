from abjad import *


def test_seqtools_repeat_sequence_to_weight_exactly_01( ):

   assert seqtools.repeat_sequence_to_weight_exactly((5, -5, -5), 23) == (5, -5, -5, 5, -3)
